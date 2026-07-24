import pytest
from fastapi import HTTPException
from jose import jwt

from conftest import make_result
from core.config import settings
from core.middleware import get_current_user
from core.security import ALGORITHM, create_access_token


@pytest.mark.asyncio
async def test_get_current_user_returns_user_for_valid_token(mock_db, mock_user):
    mock_db.execute.return_value = make_result(scalar=mock_user)
    token = create_access_token(data={"sub": str(mock_user.id)})

    user = await get_current_user(token=token, db=mock_db)

    assert user.id == mock_user.id
    mock_db.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_current_user_rejects_malformed_token(mock_db):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token="not-a-real-jwt", db=mock_db)

    assert exc_info.value.status_code == 401
    mock_db.execute.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_current_user_rejects_token_without_subject(mock_db):
    token = jwt.encode({"foo": "bar"}, settings.SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token, db=mock_db)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_rejects_unknown_user_id(mock_db):
    mock_db.execute.return_value = make_result(scalar=None)
    token = create_access_token(data={"sub": "999"})

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=token, db=mock_db)

    assert exc_info.value.status_code == 401
