from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, verify_password
from db.models import User
from schemas.auth import UserCreate


async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def google_auth_user(
    db: AsyncSession, google_id: str, email: str, full_name: str | None
) -> User:
    """
    Authenticate or register a user using Google OAuth.
    - Tries to find an existing user by Google ID first, then by email to link accounts,
    - creates a new user if no matches are found.
    """
    result = await db.execute(select(User).where(User.google_id == google_id))
    user = result.scalar_one_or_none()
    if user:
        return user

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        user.google_id = google_id  # type: ignore[assignment]
        user.auth_provider = "google"  # type: ignore[assignment]
        await db.commit()
        await db.refresh(user)
        return user

    # Create new Google user
    user = User(
        email=email,
        hashed_password=None,
        full_name=full_name,
        google_id=google_id,
        auth_provider="google",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
