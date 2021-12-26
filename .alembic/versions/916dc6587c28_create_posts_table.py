"""create posts table

Revision ID: 916dc6587c28
Revises: 
Create Date: 2021-12-19 12:14:12.013763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '916dc6587c28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table("posts")
