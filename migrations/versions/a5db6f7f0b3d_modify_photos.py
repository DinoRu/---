"""modify photos

Revision ID: a5db6f7f0b3d
Revises: 0e47d88cc76b
Create Date: 2025-06-11 12:49:13.820428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5db6f7f0b3d'
down_revision: Union[str, None] = '0e47d88cc76b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
