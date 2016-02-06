"""empty message

Revision ID: 16f11fc2c7e4
Revises: 9975799c2b8
Create Date: 2016-02-02 19:24:50.744280

"""

# revision identifiers, used by Alembic.
revision = '16f11fc2c7e4'
down_revision = '9975799c2b8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('group', sa.Column('start_date', sa.Date))
    op.add_column('group', sa.Column('start_time', sa.Time))
    op.add_column('group', sa.Column('active', sa.Boolean))


def downgrade():
    op.drop_column('group', 'start_date')
    op.drop_column('group', 'start_time')
    op.drop_column('group', 'active')
