"""create user table

Revision ID: 342016cad6bb
Revises: 6db9c9ed02e8
Create Date: 2023-03-04 22:37:47.115049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '342016cad6bb'
down_revision = '6db9c9ed02e8'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass