import hashlib
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import FaqChunk
from tools.embeddings import embed_document

"""
Service for indexing and parsing the FAQ text, which is stored in markdown files.
The FAQ is expected to be in the backend/faq directory, 
with each entry in a markdown file starting with a heading like '### [id: entry-id]', followed by **question** on the next line, and then the answer text.
The service provides functions to parse the markdown, validate entries, and index them into the database with embeddings.
"""

FAQ_DIR = Path(__file__).resolve().parent.parent / "faq"

# Matches a heading line like: ### [id: cv-upload]
_ENTRY_RE = re.compile(r"^###\s*\[id:\s*(.*?)\s*\]\s*$", re.MULTILINE)
# Validates id format: must start with lowercase letter or digit, followed by lowercase, digits, or hyphens
_VALID_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

_BOLD_QUESTION_RE = re.compile(r"^\*\*(.+)\*\*$")


class FaqParseError(Exception):
    """Raised when the corpus is malformed. Fails startup deliberately."""


@dataclass(frozen=True)
class FaqEntry:
    entry_id: str
    question: str
    answer: str

    @property
    def content_hash(self) -> str:
        """sha256 of question + answer, so one edited entry re-embeds alone."""
        payload = f"{self.question}{self.answer}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


def parse_markdown(text: str, source: str = "<string>") -> list[FaqEntry]:
    """
    Parse a markdown string into a list of FaqEntry objects.
    Raises FaqParseError if the format is invalid.
    """

    matches = list(_ENTRY_RE.finditer(text))
    if not matches:
        raise FaqParseError(f"{source}: no entries found (expected '### [id: slug]')")

    entries: list[FaqEntry] = []
    for index, match in enumerate(matches):
        entry_id = match.group(1)

        if not _VALID_ID_RE.match(entry_id):
            raise FaqParseError(
                f"{source}: entry id '{entry_id}' must contain only lowercase letters, "
                f"digits, and hyphens (must start with a letter or digit)"
            )

        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        if not body:
            raise FaqParseError(f"{source}: entry '{entry_id}' has no body")

        lines = body.splitlines()
        question_match = _BOLD_QUESTION_RE.match(lines[0].strip())
        if not question_match:
            raise FaqParseError(
                f"{source}: entry '{entry_id}' must start with a bold question line "
                f"like '**How do I ...?**', got {lines[0].strip()!r}"
            )

        answer = "\n".join(lines[1:]).strip()
        if not answer:
            raise FaqParseError(f"{source}: entry '{entry_id}' has no answer text")

        entries.append(
            FaqEntry(
                entry_id=entry_id,
                question=question_match.group(1).strip(),
                answer=answer,
            )
        )

    _reject_duplicates(entries, source)
    return entries


def _reject_duplicates(entries: list[FaqEntry], source: str) -> None:
    seen: set[str] = set()
    for entry in entries:
        if entry.entry_id in seen:
            raise FaqParseError(f"{source}: duplicate entry id '{entry.entry_id}'")
        seen.add(entry.entry_id)


def load_corpus(directory: Path = FAQ_DIR) -> list[FaqEntry]:
    """Load FAQ markdown files without indexing the calibration question set."""
    paths = sorted(path for path in directory.glob("*.md") if path.name == "faq.md")
    if not paths:
        raise FaqParseError(f"no markdown files found in {directory}")

    entries: list[FaqEntry] = []
    for path in paths:
        entries.extend(
            parse_markdown(path.read_text(encoding="utf-8"), source=path.name)
        )

    _reject_duplicates(entries, str(directory))
    return entries


@dataclass
class IndexSummary:
    added: int = 0
    updated: int = 0
    removed: int = 0
    unchanged: int = 0

    def __str__(self) -> str:
        return (
            f"FAQ index: {self.added} added, {self.updated} updated, "
            f"{self.removed} removed, {self.unchanged} unchanged"
        )


async def index_faq(
    db: AsyncSession, entries: list[FaqEntry] | None = None
) -> IndexSummary:
    """
    Index the FAQ corpus into the database, embedding each entry.
    Hashing is per entry, not corpus-wide, so fixing one typo costs one embedding
    call instead of re-embedding everything.

    """
    if entries is None:
        entries = load_corpus()

    rows = (await db.execute(select(FaqChunk.entry_id, FaqChunk.content_hash))).all()
    existing = {row[0]: row[1] for row in rows}

    summary = IndexSummary()

    for entry in entries:
        stored_hash = existing.get(entry.entry_id)

        if stored_hash == entry.content_hash:
            summary.unchanged += 1
            continue

        vector = await embed_document(f"{entry.question}\n\n{entry.answer}")

        if stored_hash is None:
            db.add(
                FaqChunk(
                    entry_id=entry.entry_id,
                    question=entry.question,
                    answer=entry.answer,
                    content_hash=entry.content_hash,
                    embedding=vector,
                    updated_at=datetime.utcnow(),
                )
            )
            summary.added += 1
        else:
            await db.execute(
                update(FaqChunk)
                .where(FaqChunk.entry_id == entry.entry_id)
                .values(
                    question=entry.question,
                    answer=entry.answer,
                    content_hash=entry.content_hash,
                    embedding=vector,
                    updated_at=datetime.utcnow(),
                )
            )
            summary.updated += 1

    current_ids = {entry.entry_id for entry in entries}
    orphaned = [entry_id for entry_id in existing if entry_id not in current_ids]
    if orphaned:
        await db.execute(delete(FaqChunk).where(FaqChunk.entry_id.in_(orphaned)))
        summary.removed = len(orphaned)

    await db.commit()
    return summary
