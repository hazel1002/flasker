"""added password field

Revision ID: 2de58fa5e29e
Revises: 
Create Date: 2022-08-04 17:48:43.318039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2de58fa5e29e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###