"""modify tables

Revision ID: 0e47d88cc76b
Revises: dd213e2ab5d3
Create Date: 2025-06-11 12:06:54.687980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e47d88cc76b'
down_revision: Union[str, None] = 'dd213e2ab5d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
