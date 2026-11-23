from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.rate_limit import check_rate_limit, client_ip
from db.database import get_db
from services.faq_query_service import answer_question

router = APIRouter(prefix="/api/faq", tags=["faq"])

"""
endpoints for the public FAQ chatbot. No auth by design.
- `POST /api/faq/ask`: Ask a question to the FAQ chatbot. Returns
    answer, grounded status, and sources. Requires ENABLE_FAQ_CHAT=true in .env.
"""


async def require_faq_enabled() -> None:
    """404 when the feature is off"""
    if not settings.ENABLE_FAQ_CHAT:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")


async def enforce_rate_limit(request: Request) -> None:
    """Per-IP cost guard. This is the only /api route without an auth check."""
    check_rate_limit(client_ip(request))


class FaqAskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


class FaqAskResponse(BaseModel):
    answer: str
    grounded: bool
    sources: list[str]


@router.post(
    "/ask",
    response_model=FaqAskResponse,
    # Order matters: a disabled feature must 404 without spending a bucket slot.
    dependencies=[Depends(require_faq_enabled), Depends(enforce_rate_limit)],
)
async def ask(
    body: FaqAskRequest,
    db: AsyncSession = Depends(get_db),
) -> FaqAskResponse:
    result = await answer_question(db, body.question)
    return FaqAskResponse(
        answer=result.answer,
        grounded=result.grounded,
        sources=result.sources,
    )
