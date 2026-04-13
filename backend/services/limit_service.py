from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from services.profile_service import get_or_create_profile

DAILY_ANALYSIS_LIMIT = 3


async def check_and_increment_daily_limit(user_id: int, db: AsyncSession) -> None:
    """
    Enforce the daily analysis cap of DAILY_ANALYSIS_LIMIT per user.

    Resets the counter if the stored reset date differs from today, then raises
    HTTP 429 if the limit is already reached. Otherwise increments and commits.
    """
    profile = await get_or_create_profile(db, user_id)
    today = date.today()

    if profile.daily_analyses_reset_date != today:
        profile.daily_analyses_used = 0
        profile.daily_analyses_reset_date = today

    if profile.daily_analyses_used >= DAILY_ANALYSIS_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Daily analysis limit reached ({DAILY_ANALYSIS_LIMIT}/day). Try again tomorrow.",
        )

    profile.daily_analyses_used += 1
    await db.commit()
