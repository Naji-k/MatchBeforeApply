from google import genai
from google.genai.types import EmbedContentConfig
from pydantic import BaseModel

from core.config import settings

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSIONS = 768

_client: genai.Client | None = None


class GroundedAnswer(BaseModel):
    """Structured reply from the FAQ model."""

    answer: str = ""
    answered: bool = False


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    return _client


async def _embed(text: str) -> list[float]:
    response = await _get_client().aio.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSIONS),
    )
    return list(response.embeddings[0].values)


async def embed_document(text: str) -> list[float]:
    """Embed corpus text for storage."""
    return await _embed(f"title: none | text: {text}")


async def embed_query(text: str) -> list[float]:
    """Embed a user question for retrieval."""
    return await _embed(f"task: search result | query: {text}")


async def generate_answer(prompt: str) -> GroundedAnswer:
    """
    Generate an answer to a user question using the provided prompt.
    The prompt should include the user question and any relevant context
    The response will be a JSON object with the answer and whether it was grounded in the context.
    """
    response = await _get_client().aio.models.generate_content(
        model=settings.MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": GroundedAnswer,
        },
    )
    return GroundedAnswer.model_validate_json(response.text or "{}")
