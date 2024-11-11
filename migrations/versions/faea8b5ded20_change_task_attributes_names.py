"""Change Task attributes names.

Revision ID: faea8b5ded20
Revises: 7becc7906068
Create Date: 2024-11-11 13:13:48.262172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'faea8b5ded20'
down_revision: Union[str, None] = '7becc7906068'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('dispatcher_name', sa.String(), nullable=False))
    op.add_column('tasks', sa.Column('location', sa.String(), nullable=False))
    op.add_column('tasks', sa.Column('planner_date', sa.DateTime(), nullable=False))
    op.add_column('tasks', sa.Column('work_type', sa.String(), nullable=False))
    op.add_column('tasks', sa.Column('voltage_class', sa.Float(), nullable=False))
    op.drop_column('tasks', 'address')
    op.drop_column('tasks', 'king_of_work')
    op.drop_column('tasks', 'obj_name')
    op.drop_column('tasks', 'according_date')
    op.drop_column('tasks', 'voltage')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('voltage', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('tasks', sa.Column('according_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('tasks', sa.Column('obj_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('tasks', sa.Column('king_of_work', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('tasks', sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('tasks', 'voltage_class')
    op.drop_column('tasks', 'work_type')
    op.drop_column('tasks', 'planner_date')
    op.drop_column('tasks', 'location')
    op.drop_column('tasks', 'dispatcher_name')
    # ### end Alembic commands ###
