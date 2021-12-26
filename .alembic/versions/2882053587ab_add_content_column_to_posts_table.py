"""add content column to posts table

Revision ID: 2882053587ab
Revises: 916dc6587c28
Create Date: 2021-12-19 12:42:19.294197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2882053587ab'
down_revision = '916dc6587c28'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )


def downgrade():
    op.drop_column("posts", "content")
