"""replace photo urls with photos array

Revision ID: 9c8925867860
Revises: a5db6f7f0b3d
Create Date: 2025-06-11 12:54:58.567424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import table, update

# revision identifiers, used by Alembic.
revision: str = '9c8925867860'
down_revision: Union[str, None] = 'a5db6f7f0b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Ajouter la colonne `photos` avant suppression
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(
            sa.Column("photos", pg.ARRAY(sa.VARCHAR()), nullable=True)
        )

    # Déclarer les colonnes nécessaires pour faire le transfert
    tasks_table = table(
        "tasks",
        sa.Column("photo_url_1", sa.VARCHAR),
        sa.Column("photo_url_2", sa.VARCHAR),
        sa.Column("photo_url_3", sa.VARCHAR),
        sa.Column("photo_url_4", sa.VARCHAR),
        sa.Column("photo_url_5", sa.VARCHAR),
        sa.Column("photos", pg.ARRAY(sa.VARCHAR)),
    )

    bind = op.get_bind()

    # Mettre à jour les données en copiant dans la nouvelle colonne `photos`
    bind.execute(
        update(tasks_table).values(
            photos=sa.func.array_remove(
                pg.array([
                    tasks_table.c.photo_url_1,
                    tasks_table.c.photo_url_2,
                    tasks_table.c.photo_url_3,
                    tasks_table.c.photo_url_4,
                    tasks_table.c.photo_url_5,
                ]),
                None
            )
        )
    )

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_column("photo_url_1")
        batch_op.drop_column("photo_url_2")
        batch_op.drop_column("photo_url_3")
        batch_op.drop_column("photo_url_4")
        batch_op.drop_column("photo_url_5")

        # # Ajouter la nouvelle colonne photos (ARRAY)
        # batch_op.add_column(
        #     sa.Column("photos", pg.ARRAY(sa.VARCHAR()), nullable=True)
        # )



        # Ajouter la contrainte
        batch_op.create_check_constraint(
            "photos_length_check",
            "array_length(photos, 1) BETWEEN 2 AND 5"
        )


def downgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint("photos_length_check", type_="check")
        batch_op.drop_column("photos")

        # Réajouter les anciennes colonnes
        batch_op.add_column(sa.Column("photo_url_5", sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column("photo_url_4", sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column("photo_url_3", sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column("photo_url_2", sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column("photo_url_1", sa.VARCHAR(), nullable=True))
