"""add jd_url to applications

Revision ID: a3b7c9d12ef4
Revises: f238bb5cbb22
Create Date: 2026-04-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3b7c9d12ef4'
down_revision: Union[str, Sequence[str], None] = 'f238bb5cbb22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('applications', sa.Column('jd_url', sa.String(length=2048), nullable=True))


def downgrade() -> None:
    op.drop_column('applications', 'jd_url')
