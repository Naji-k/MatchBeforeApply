from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import UserProfile
from schemas.profile import ProfileUpdate


async def get_or_create_profile(db: AsyncSession, user_id: int) -> UserProfile:
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if profile is None:
        profile = UserProfile(user_id=user_id)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile


async def update_profile(
    db: AsyncSession, user_id: int, data: ProfileUpdate
) -> UserProfile:
    profile = await get_or_create_profile(db, user_id)
    profile.cv_text = data.cv_text
    profile.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(profile)
    return profile
