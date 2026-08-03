import logging
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import FaqChunk, FaqQueryLog
from tools.embeddings import embed_query, generate_answer

logger = logging.getLogger(__name__)

"""Service for answering user questions using the FAQ corpus. Uses pgvector to retrieve relevant entries, 
then generates a response using the reference entries as context."""

DISTANCE_THRESHOLD = 0.38
TOP_K = 4

REFUSAL_TEXT = "I don't know the answer to that question. Please try rephrasing it or use the feedback button to ask for help."

_PROMPT = """You answer questions about the MatchBeforeApply web app.

Use ONLY the reference entries below. Be concise and friendly. Do not mention the
reference entries, their ids, or that you were given context.

Set "answered" to true only when the reference entries actually contain the
answer. If they do not, set "answered" to false and leave "answer" empty rather
than guessing.

Reference entries:
{context}

User question: {question}
"""


@dataclass(frozen=True)
class FaqAnswer:
    answer: str
    grounded: bool
    sources: list[str]


async def _log_query(
    db: AsyncSession,
    question: str,
    top_distance: float | None,
    result: FaqAnswer,
    rows: Sequence[Row],
) -> None:
    """Record the query for retrieval analytics.
    Logs the question, the distance to the closest FAQ entry, whether the answer was grounded in the FAQ,
    and the list of matched entry_ids.
    """
    try:
        db.add(
            FaqQueryLog(
                question=question[:500],
                top_distance=top_distance,
                grounded=result.grounded,
                matched_ids=[r.entry_id for r in rows],
            )
        )
        await db.commit()
    except Exception:
        logger.exception("failed to write faq query log")
        await db.rollback()


async def answer_question(db: AsyncSession, question: str) -> FaqAnswer:
    """
    Answer a user question by retrieving relevant FAQ entries and generating a response.
        Returns a FaqAnswer, whether it is grounded in the FAQ,
        and the list of source entry_ids used to generate the answer.
    If no relevant entries are found, returns a refusal answer.

    """
    query_vector = await embed_query(question)

    rows = (
        await db.execute(
            select(
                FaqChunk.entry_id,
                FaqChunk.question,
                FaqChunk.answer,
                FaqChunk.embedding.cosine_distance(query_vector).label("distance"),
            )
            .order_by("distance")
            .limit(TOP_K)
        )
    ).all()

    top_distance = rows[0].distance if rows else None
    logger.info("FAQ query: %r top_distance=%s", question, top_distance)

    if not rows or top_distance > DISTANCE_THRESHOLD:
        result = FaqAnswer(answer=REFUSAL_TEXT, grounded=False, sources=[])
    else:
        kept = [row for row in rows if row.distance <= DISTANCE_THRESHOLD]
        context = "\n\n".join(f"{row.question}\n{row.answer}" for row in kept)

        result = await generate_answer(
            _PROMPT.format(context=context, question=question)
        )
        result = FaqAnswer(
            answer=result.answer if result.answered else REFUSAL_TEXT,
            grounded=result.answered,
            sources=[r.entry_id for r in kept] if result.answered else [],
        )
    await _log_query(db, question, top_distance, result, rows)
    return result
