"""Database creation

Revision ID: 38b29dd0231e
Revises: 154ccdd8c531
Create Date: 2024-03-04 22:48:29.620191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '38b29dd0231e'
down_revision: Union[str, None] = '154ccdd8c531'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reminder')
    op.drop_table('new_dict')
    op.drop_table('all_dict')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('all_dict',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('word', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('count_answer', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='all_dict_pkey'),
    sa.UniqueConstraint('word', name='unique_email')
    )
    op.create_table('new_dict',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('word', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('count_answer', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='new_dict_pkey')
    )
    op.create_table('reminder',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('state', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='reminder_pkey')
    )
    # ### end Alembic commands ###