"""add last few column to posts table

Revision ID: 14997651eedc
Revises: 83498179f5a1
Create Date: 2023-03-04 22:48:22.619044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14997651eedc'
down_revision = '83498179f5a1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass