from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.middleware import get_current_user
from db.database import get_db
from db.models import User
from schemas.profile import ProfileResponse, ProfileUpdate
from services.profile_service import get_or_create_profile, update_profile
from tools.pdf_parser import extract_text_from_pdf

router = APIRouter(prefix="/api/profile", tags=["profile"])
"""
Endpoints for managing user profile and CV text.
- `GET /api/profile`: Retrieve the user's profile, creating it if it doesn't exist.
- `PUT /api/profile`: Update the user's CV text directly (expects plain text).
- `POST /api/profile/upload-cv`: Upload a CV as a PDF file; extracts
"""


@router.get("", response_model=ProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_or_create_profile(db, current_user.id)


@router.put("", response_model=ProfileResponse)
async def upsert_profile(
    data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_profile(db, current_user.id, data)


@router.post("/upload-cv", response_model=ProfileResponse)
async def upload_cv(
    cv_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    file_bytes = await cv_file.read()
    try:
        cv_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {e}")
    if not cv_text.strip():
        raise HTTPException(status_code=400, detail="PDF appears empty or unreadable.")
    return await update_profile(db, current_user.id, ProfileUpdate(cv_text=cv_text))
