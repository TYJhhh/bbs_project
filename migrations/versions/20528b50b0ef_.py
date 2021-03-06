"""empty message

Revision ID: 20528b50b0ef
Revises: ca4ef31a5c0c
Create Date: 2020-01-03 10:36:09.623905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20528b50b0ef'
down_revision = 'ca4ef31a5c0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rid', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_rid'), 'posts', ['rid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_rid'), table_name='posts')
    op.drop_table('posts')
    # ### end Alembic commands ###
