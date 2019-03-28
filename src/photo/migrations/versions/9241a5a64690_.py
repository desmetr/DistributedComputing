"""empty message

Revision ID: 9241a5a64690
Revises: 
Create Date: 2019-03-26 13:18:01.191184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9241a5a64690'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=144), nullable=True),
    sa.Column('filename', sa.String(length=144), nullable=True),
    sa.Column('user', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_photo_filename'), 'photo', ['filename'], unique=False)
    op.create_index(op.f('ix_photo_url'), 'photo', ['url'], unique=False)
    op.create_index(op.f('ix_photo_user'), 'photo', ['user'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_photo_user'), table_name='photo')
    op.drop_index(op.f('ix_photo_url'), table_name='photo')
    op.drop_index(op.f('ix_photo_filename'), table_name='photo')
    op.drop_table('photo')
    # ### end Alembic commands ###
