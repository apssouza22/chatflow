"""initial migration

Revision ID: 4b38dcceb583
Revises: 
Create Date: 2023-10-19 20:24:25.255587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b38dcceb583'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apps')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_ref', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('app_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('app_description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('app_key', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('app_model', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('app_temperature', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_ref'], ['users.id'], name='apps_user_ref_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'user_ref', name='apps_pkey'),
    sa.UniqueConstraint('user_ref', 'app_key', name='_app_key_unique'),
    sa.UniqueConstraint('user_ref', 'app_name', name='_app_name_unique')
    )
    # ### end Alembic commands ###
