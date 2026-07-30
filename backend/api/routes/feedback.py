from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel

from core.middleware import get_current_user
from db.models import User
from services.email_service import send_feedback_email
from core.config import settings


class FeedbackRequest(BaseModel):
    message: str


router = APIRouter(prefix="/api", tags=["feedback"])


@router.post("/feedback", status_code=204)
async def submit_feedback(
    body: FeedbackRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
):
    """
    Submit user feedback. The email is sent as a background task.
    """
    background_tasks.add_task(
        send_feedback_email,
        user_name=current_user.full_name or current_user.email,
        user_email=current_user.email,
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
