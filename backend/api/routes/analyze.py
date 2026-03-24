import os

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from core.middleware import get_current_user
from db.models import User
from services.analyze_service import run_analysis
from tools.pdf_parser import extract_text_from_pdf

router = APIRouter(tags=["analyze"])


@router.post("/api/analyze")
async def analyze(
    cv_file: UploadFile = File(...),
    jd_type: str = Form(...),
    jd_input: str = Form(...),
    current_user: User = Depends(get_current_user),
):
    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not configured.")

    file_bytes = await cv_file.read()
    try:
        cv_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse PDF: {e}")

    if not cv_text.strip():
        raise HTTPException(
            status_code=400, detail="PDF appears to be empty or unreadable."
        )

    return await run_analysis(cv_text, jd_type, jd_input)
