"""Add content column to posts table

Revision ID: 82173109ae9c
Revises: 41cd134a7f11
Create Date: 2026-01-11 18:34:21.976474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82173109ae9c'
down_revision: Union[str, Sequence[str], None] = '41cd134a7f11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
