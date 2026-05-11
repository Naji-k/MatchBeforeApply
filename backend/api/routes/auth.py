from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.middleware import get_current_user
from core.security import create_access_token
from db.database import get_db
from db.models import User
from schemas.auth import (
    GoogleAuthRequest,
    Token,
    UserCreate,
    UserResponse,
    VerifyEmailRequest,
)
from services.auth_service import (
    authenticate_user,
    generate_and_save_otp,
    google_auth_user,
    register_user,
    verify_otp_code,
)
from services.email_service import send_otp_email

router = APIRouter(prefix="/api/auth", tags=["auth"])
"""
Authentication endpoints:
- `POST /api/auth/register`: Register a new user with email and password.
- `POST /api/auth/login`: Authenticate user and return JWT token.
- `GET /api/auth/me`: Get current user info (requires Bearer token).
- `POST /api/auth/google`: Sign in or register with Google ID token."""


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await register_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.post("/google", response_model=Token)
async def google_login(body: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google sign-in is not configured",
        )
    try:
        id_info = id_token.verify_oauth2_token(
            body.credential,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token",
        ) from exc

    google_id: str = id_info["sub"]
    email: str = id_info.get("email", "")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account has no verified email",
        )
    full_name: str | None = id_info.get("name")

    user = await google_auth_user(db, google_id, email, full_name)
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/send-verification", status_code=204)
async def send_verification(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.is_email_verified:
        return
    otp = await generate_and_save_otp(db, current_user)
    send_otp_email(current_user.email, otp)


@router.post("/verify-email", response_model=UserResponse)
async def verify_email(
    body: VerifyEmailRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.is_email_verified:
        return current_user
    ok = await verify_otp_code(db, current_user, body.code)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired code. Please request a new one.",
        )
    await db.refresh(current_user)
    return current_user


@router.post("/demo-login")
async def demo_login(
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(
        db, settings.VITE_DEMO_USER_EMAIL, settings.VITE_DEMO_USER_PASSWORD
    )
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token)
