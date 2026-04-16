import random
import string
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, verify_password
from db.models import User
from schemas.auth import UserCreate


def _generate_otp() -> str:
    return "".join(random.choices(string.digits, k=6))


async def generate_and_save_otp(db: AsyncSession, user: User) -> str:
    otp = _generate_otp()
    user.otp_code = otp
    user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
    await db.commit()
    return otp


async def verify_otp_code(db: AsyncSession, user: User, code: str) -> bool:
    if not user.otp_code or not user.otp_expires_at:
        return False
    if user.otp_expires_at < datetime.utcnow():
        return False
    if user.otp_code != code:
        return False
    user.is_email_verified = True
    user.otp_code = None
    user.otp_expires_at = None
    await db.commit()
    return True


async def register_user(db: AsyncSession, user_in: UserCreate) -> User:
    from services.email_service import send_otp_email

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
        is_email_verified=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    try:
        otp = await generate_and_save_otp(db, user)
        send_otp_email(user.email, otp)
    except Exception:
        pass  # non-fatal — user can resend from profile

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

    # Create new Google user (auto-verified — Google guarantees email ownership)
    user = User(
        email=email,
        hashed_password=None,
        full_name=full_name,
        google_id=google_id,
        auth_provider="google",
        is_email_verified=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
