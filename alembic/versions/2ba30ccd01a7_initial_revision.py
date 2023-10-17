"""initial revision

Revision ID: 2ba30ccd01a7
Revises: 
Create Date: 2023-10-17 03:53:07.216547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.functions import now


# revision identifiers, used by Alembic.
revision: str = '2ba30ccd01a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(250), nullable=False, unique=True),
        sa.Column('password', sa.String(200)),  # TODO: hash password
        sa.Column('name', sa.String(50)),
    )

    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_ref', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('chatbot_id', sa.String(50), unique=True),
        sa.Column('message', sa.Text()),
        sa.Column('is_bot_reply', sa.Boolean()),  # TODO: needs index?
        sa.Column('createdat', sa.DateTime(), server_default=now(), index=True),  # TODO: needs index?
    )


def downgrade() -> None:
    op.drop_table('chat_messages')
    op.drop_table('users')
