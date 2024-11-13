"""remove index from task_id.

Revision ID: 078f55293274
Revises: dcd47114c77e
Create Date: 2024-11-13 23:11:06.431239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '078f55293274'
down_revision: Union[str, None] = 'dcd47114c77e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_tasks_task_id', table_name='tasks')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_tasks_task_id', 'tasks', ['task_id'], unique=False)
    # ### end Alembic commands ###
