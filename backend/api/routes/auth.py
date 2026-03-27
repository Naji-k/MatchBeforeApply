from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.middleware import get_current_user
from core.security import create_access_token
from db.database import get_db
from db.models import User
from schemas.auth import Token, UserCreate, UserResponse
from services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/api/auth", tags=["auth"])
"""
Authentication endpoints:
- `POST /api/auth/register`: Register a new user with email and password.
- `POST /api/auth/login`: Authenticate user and return JWT token.
- `GET /api/auth/me`: Get current user info (requires Bearer token)."""


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


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
