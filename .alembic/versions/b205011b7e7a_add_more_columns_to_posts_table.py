"""add more columns to posts table

Revision ID: b205011b7e7a
Revises: 2156ccf05ed5
Create Date: 2021-12-19 13:57:15.538949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b205011b7e7a'
down_revision = '2156ccf05ed5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts", 
        sa.Column("published", sa.Boolean(), server_default='TRUE', nullable=False)
    )
    op.add_column(
        "posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
