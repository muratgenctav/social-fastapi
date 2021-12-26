"""sync with models

Revision ID: ae14d8e4eff9
Revises: b205011b7e7a
Create Date: 2021-12-19 14:22:30.074536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae14d8e4eff9'
down_revision = 'b205011b7e7a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'post_id')
    )


def downgrade():
    op.drop_table('votes')
