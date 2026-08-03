"""add faq_query_logs

Revision ID: 7d18f3cd2be3
Revises: b8e1f4a27c30
Create Date: 2026-08-03

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7d18f3cd2be3"
down_revision: Union[str, Sequence[str], None] = "b8e1f4a27c30"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Retrieval analytics for the FAQ chatbot.

    Deliberately unguarded, unlike the faq_chunks migration: this table holds no
    Vector column, so it creates fine on a Postgres without pgvector. It also has
    no FK to faq_chunks -- on such a server that table does not exist, and the
    logs must still be writable.
    """
    op.create_table(
        "faq_query_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("top_distance", sa.Float(), nullable=True),
        sa.Column("grounded", sa.Boolean(), nullable=False),
        sa.Column(
            "matched_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_faq_query_logs_id"), "faq_query_logs", ["id"])


def downgrade() -> None:
    op.drop_index(op.f("ix_faq_query_logs_id"), table_name="faq_query_logs")
    op.drop_table("faq_query_logs")
