from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.middleware import get_current_user
from db.database import get_db
from db.models import User
from services.email_service import send_feedback_email
from core.config import settings


class FeedbackRequest(BaseModel):
    message: str


router = APIRouter(prefix="/api", tags=["feedback"])
# Optional user dependency: returns the caller if they sent a usable token, else None.
_optional_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def _optional_user(
    token: str | None = Depends(_optional_scheme),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """
    Optional user dependency: returns the caller if they sent a usable token, else None.
    This is used for the feedback endpoint, which is open to anonymous callers.
    """
    if not token:
        return None
    try:
        return await get_current_user(token=token, db=db)
    except (HTTPException, ValueError):
        return None


@router.post("/feedback", status_code=204)
async def submit_feedback(
    body: FeedbackRequest,
    background_tasks: BackgroundTasks,
    current_user: User | None = Depends(_optional_user),
):
    if not current_user:
        current_user_name = "Anonymous"
        current_user_email = ""
    else:
        current_user_name = current_user.full_name or current_user.email
        current_user_email = current_user.email
    background_tasks.add_task(
        send_feedback_email,
        user_name=current_user_name,
        user_email=current_user_email,
        message=body.message,
    )


@router.get("/config", status_code=200)
async def get_config():
    return {
        "VITE_GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
        "VITE_ENABLE_SIGNUP": settings.VITE_ENABLE_SIGNUP,
        "VITE_DEMO_USER": settings.VITE_DEMO_USER,
        "PUBLIC_GA_MEASUREMENT_ID": settings.PUBLIC_GA_MEASUREMENT_ID,
        "ENABLE_FAQ_CHAT": settings.ENABLE_FAQ_CHAT,
    }
