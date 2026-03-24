from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    cv_text: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    cv_text: str
