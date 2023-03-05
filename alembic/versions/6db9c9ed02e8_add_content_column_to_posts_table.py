"""add content column to posts table

Revision ID: 6db9c9ed02e8
Revises: c31205ab7c1e
Create Date: 2023-03-04 22:29:18.842190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6db9c9ed02e8'
down_revision = 'c31205ab7c1e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
