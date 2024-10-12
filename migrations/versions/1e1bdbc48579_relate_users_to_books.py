"""Relate users to books

Revision ID: 1e1bdbc48579
Revises: 0361983afabb
Create Date: 2024-10-12 02:58:51.663306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '1e1bdbc48579'
down_revision: Union[str, None] = '0361983afabb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('user_uid', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'books', 'users', ['user_uid'], ['uid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'user_uid')
    # ### end Alembic commands ###