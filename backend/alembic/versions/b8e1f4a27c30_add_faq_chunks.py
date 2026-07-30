"""add faq_chunks

Revision ID: b8e1f4a27c30
Revises: a3b7c9d12ef4
Create Date: 2026-07-29

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = "b8e1f4a27c30"
down_revision: Union[str, Sequence[str], None] = "a3b7c9d12ef4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _pgvector_available(conn) -> bool:
    """Whether this server can install the vector extension at all.

    entrypoint.sh runs `alembic upgrade head` before uvicorn starts, so an
    unconditional CREATE EXTENSION would fail the migration, fail the boot, and
    take the whole app down for anyone whose Postgres lacks pgvector -- including
    people who never enabled ENABLE_FAQ_CHAT. Alembic cannot read application
    settings, so the guard has to be on capability, not on the feature flag.
    """
    return bool(
        conn.execute(
            sa.text("SELECT 1 FROM pg_available_extensions WHERE name = 'vector'")
        ).scalar()
    )


def upgrade() -> None:
    conn = op.get_bind()
    if not _pgvector_available(conn):
        return

    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "faq_chunks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entry_id", sa.String(length=255), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("embedding", Vector(768), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_faq_chunks_id"), "faq_chunks", ["id"])
    op.create_index(
        op.f("ix_faq_chunks_entry_id"), "faq_chunks", ["entry_id"], unique=True
    )


def downgrade() -> None:
    conn = op.get_bind()
    if not _pgvector_available(conn):
        return

    op.drop_index(op.f("ix_faq_chunks_entry_id"), table_name="faq_chunks")
    op.drop_index(op.f("ix_faq_chunks_id"), table_name="faq_chunks")
    op.drop_table("faq_chunks")
