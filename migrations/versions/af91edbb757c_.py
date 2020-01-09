"""empty message

Revision ID: af91edbb757c
Revises: 52395ced0e22
Create Date: 2020-01-09 20:10:22.070063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af91edbb757c'
down_revision = '52395ced0e22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('username')
    )
    op.drop_table('collections')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comments', 'posts', ['post_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['uid'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['uid'], ['id'])
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'posts', ['post_id'], ['id'])
    op.create_foreign_key(None, 'comments', 'users', ['user_id'], ['id'])
    op.create_table('collections',
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.drop_table('admin')
    # ### end Alembic commands ###