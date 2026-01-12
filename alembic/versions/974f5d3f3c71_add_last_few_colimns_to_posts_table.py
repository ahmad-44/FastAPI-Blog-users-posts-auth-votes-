"""add last few colimns to posts table

Revision ID: 974f5d3f3c71
Revises: ef076f190321
Create Date: 2026-01-11 19:03:47.834590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '974f5d3f3c71'
down_revision: Union[str, Sequence[str], None] = 'ef076f190321'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
