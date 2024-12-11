"""add mutations to base mechanics

Revision ID: d834ca5f3c12
Revises: 375c38ce0d9d
Create Date: 2024-12-11 10:27:04.613094

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d834ca5f3c12"
down_revision: Union[str, None] = "375c38ce0d9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("base_mechanics", sa.Column("mutations", sa.INTEGER()))
    op.add_column("base_mechanics", sa.Column("mental_mutations", sa.INTEGER()))
    op.add_column("base_mechanics", sa.Column("physical_mutations", sa.INTEGER()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("base_mechanics", "physical_mutations")
    op.drop_column("base_mechanics", "mental_mutations")
    op.drop_column("base_mechanics", "mutations")
    # ### end Alembic commands ###
