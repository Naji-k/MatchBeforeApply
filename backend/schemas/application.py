from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel

from db.models import ApplicationStatus, CommentType


class ApplicationCreate(BaseModel):
    jd_source: str
    jd_type: Literal["url", "text"]
    jd_text: Optional[str] = None
    run_analysis: bool = True


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    cover_letter: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    jd_source: str
    jd_type: Optional[str] = None
    jd_text: Optional[str] = None
    match_score: Optional[int] = None
    match_breakdown: Optional[Dict[str, Any]] = None
    ats_tips: Optional[Dict[str, Any]] = None
    jd_data: Optional[Dict[str, Any]] = None
    cover_letter: Optional[str] = None
    status: ApplicationStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    type: CommentType
    question: Optional[str] = None
    comment: str


class CommentResponse(BaseModel):
    id: int
    application_id: int
    user_id: int
    type: CommentType
    question: Optional[str] = None
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True
