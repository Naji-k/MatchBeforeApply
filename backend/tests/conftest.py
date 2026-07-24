from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.middleware import get_current_user
from core.security import create_access_token, hash_password
from db.database import get_db
from db.models import Application, ApplicationStatus, User, UserProfile
from main import app


def make_result(scalar=None, scalars_list=None):
    """Stand-in for the Result object returned by AsyncSession.execute()."""
    result = MagicMock()
    result.scalar_one_or_none.return_value = scalar
    result.scalars.return_value.all.return_value = scalars_list or []
    return result


async def _fake_refresh(obj):
    """Mimic AsyncSession.refresh() populating DB-generated defaults on a new row."""
    if getattr(obj, "id", None) is None:
        obj.id = 1
    if hasattr(obj, "created_at") and obj.created_at is None:
        obj.created_at = datetime(2026, 1, 1, 12, 0, 0)
    if hasattr(obj, "updated_at") and obj.updated_at is None:
        obj.updated_at = datetime(2026, 1, 1, 12, 0, 0)
    if hasattr(obj, "status") and obj.status is None:
        obj.status = ApplicationStatus.open


@pytest.fixture
def mock_db():
    db = AsyncMock(spec=AsyncSession)
    db.refresh.side_effect = _fake_refresh
    return db


@pytest.fixture
def mock_user():
    return User(
        id=1,
        email="jane@example.com",
        hashed_password=hash_password("correct-password"),
        full_name="Jane Doe",
        auth_provider="local",
        is_email_verified=True,
        created_at=datetime(2026, 1, 1, 9, 0, 0),
    )


@pytest.fixture
def auth_token(mock_user):
    return create_access_token(data={"sub": str(mock_user.id)})


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def mock_profile(mock_user):
    return UserProfile(
        id=1,
        user_id=mock_user.id,
        cv_text="Experienced backend engineer skilled in Python and FastAPI.",
        daily_analyses_used=0,
        daily_analyses_reset_date=date.today(),
        updated_at=datetime(2026, 1, 1, 9, 0, 0),
    )


@pytest.fixture
def mock_application(mock_user):
    return Application(
        id=10,
        user_id=mock_user.id,
        jd_source="Senior Backend Engineer role at Acme Corp.",
        jd_type="text",
        jd_text="Senior Backend Engineer role at Acme Corp.",
        jd_url=None,
        match_score=None,
        match_breakdown=None,
        ats_tips=None,
        jd_data=None,
        cover_letter=None,
        status=ApplicationStatus.open,
        created_at=datetime(2026, 1, 2, 10, 0, 0),
        updated_at=datetime(2026, 1, 2, 10, 0, 0),
    )


@pytest_asyncio.fixture
async def client(mock_db):
    """Only the DB dependency is overridden — exercises real JWT/auth logic."""
    app.dependency_overrides[get_db] = lambda: mock_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def authed_client(mock_db, mock_user):
    """DB and current-user both overridden — use when auth itself isn't under test."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: mock_user
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
