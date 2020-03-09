"""empty message

Revision ID: d4af986e051d
Revises: 97867a87ea58
Create Date: 2020-03-08 14:28:55.206586

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd4af986e051d'
down_revision = '97867a87ea58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('slug', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('summary', sa.String(length=256), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('slug', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug'),
    sa.UniqueConstraint('title')
    )
    op.drop_index('slug', table_name='post')
    op.drop_index('title', table_name='post')
    op.drop_table('post')
    op.drop_index('name', table_name='category')
    op.drop_index('slug', table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('description', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('slug', mysql.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('slug', 'category', ['slug'], unique=True)
    op.create_index('name', 'category', ['name'], unique=True)
    op.create_table('post',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=128), nullable=False),
    sa.Column('summary', mysql.VARCHAR(length=256), nullable=True),
    sa.Column('content', mysql.TEXT(), nullable=False),
    sa.Column('slug', mysql.VARCHAR(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('title', 'post', ['title'], unique=True)
    op.create_index('slug', 'post', ['slug'], unique=True)
    op.drop_table('posts')
    op.drop_table('categories')
    # ### end Alembic commands ###
