"""init

Revision ID: 684bd823e198
Revises: 
Create Date: 2024-10-09 11:56:18.955611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '684bd823e198'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('firstname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('lastname', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.alter_column('books', 'published_date',
               existing_type=sa.VARCHAR(),
               type_=sa.Date(),
               existing_nullable=False)
    op.alter_column('books', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('books', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('books', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('books', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('books', 'published_date',
               existing_type=sa.Date(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.drop_table('users')
    # ### end Alembic commands ###