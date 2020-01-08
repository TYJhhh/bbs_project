"""empty message

Revision ID: 64108eb7328b
Revises: 27611f71395d
Create Date: 2020-01-06 20:57:45.342237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64108eb7328b'
down_revision = '27611f71395d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###
