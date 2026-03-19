"""add content column to posts table

Revision ID: d2fe7be39080
Revises: 5204cc8e92a2
Create Date: 2026-03-18 23:37:43.934424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2fe7be39080'
down_revision: Union[str, Sequence[str], None] = '5204cc8e92a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
