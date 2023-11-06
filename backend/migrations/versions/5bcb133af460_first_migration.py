"""First migration

Revision ID: 5bcb133af460
Revises: 
Create Date: 2023-11-05 23:02:54.673437

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bcb133af460'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event')
    op.drop_table('user')
    op.drop_table('event_tags')
    op.drop_table('user_interested_event')
    op.drop_table('tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_interested_event',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('event_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_tags',
    sa.Column('event_id', sa.INTEGER(), nullable=False),
    sa.Column('tag_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('event_id', 'tag_id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=255), nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=255), nullable=False),
    sa.Column('password_salt', sa.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('event',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('location', sa.VARCHAR(length=255), nullable=False),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=False),
    sa.Column('author_id', sa.INTEGER(), nullable=True),
    sa.Column('is_published', sa.BOOLEAN(), nullable=False),
    sa.Column('like_count', sa.INTEGER(), nullable=True),
    sa.Column('image', sa.BLOB(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
