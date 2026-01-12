"""add user table

Revision ID: 5eb035642265
Revises: 82173109ae9c
Create Date: 2026-01-11 18:40:31.536108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5eb035642265'
down_revision: Union[str, Sequence[str], None] = '82173109ae9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()'))
    )   


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
