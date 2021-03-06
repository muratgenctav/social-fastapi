"""add foreign key to posts table

Revision ID: 2156ccf05ed5
Revises: 51b908817bb9
Create Date: 2021-12-19 13:25:35.200783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2156ccf05ed5'
down_revision = '51b908817bb9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
