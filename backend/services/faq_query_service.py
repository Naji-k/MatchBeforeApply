import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import FaqChunk
from tools.embeddings import embed_query, generate_answer

logger = logging.getLogger(__name__)

"""Service for answering user questions using the FAQ corpus. Uses pgvector to retrieve relevant entries, 
then generates a response using the reference entries as context."""

DISTANCE_THRESHOLD = 0.6
TOP_K = 4

REFUSAL_TEXT = "I can only answer questions about this app."

_PROMPT = """You answer questions about the MatchBeforeApply web app.

Use ONLY the reference entries below. If they do not contain the answer, say you
do not know rather than guessing. Be concise and friendly. Do not mention the
reference entries, their ids, or that you were given context.

Reference entries:
{context}

User question: {question}
"""


@dataclass(frozen=True)
class FaqAnswer:
    answer: str
    grounded: bool
    sources: list[str]


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
        return FaqAnswer(answer=REFUSAL_TEXT, grounded=False, sources=[])

    kept = [row for row in rows if row.distance <= DISTANCE_THRESHOLD]
    context = "\n\n".join(f"{row.question}\n{row.answer}" for row in kept)

    answer = await generate_answer(_PROMPT.format(context=context, question=question))
    return FaqAnswer(
        answer=answer,
        grounded=True,
        sources=[row.entry_id for row in kept],
    )
