"""add phone number column to users table

Revision ID: a4448cba6766
Revises: ae14d8e4eff9
Create Date: 2021-12-19 14:34:08.439646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4448cba6766'
down_revision = 'ae14d8e4eff9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'phone_number')
