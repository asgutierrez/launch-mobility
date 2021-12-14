"""empty message

Revision ID: 4b2af5f8034e
Revises: 72f99be8cbc1
Create Date: 2021-12-12 22:10:02.532208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b2af5f8034e'
down_revision = '72f99be8cbc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zipcoderank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zip_code', sa.String(length=5), nullable=False),
    sa.Column('county', sa.String(length=250), nullable=True),
    sa.Column('mode', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('zip_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('zipcoderank')
    # ### end Alembic commands ###
