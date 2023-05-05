"""empty message

Revision ID: 865161dee141
Revises: b7bbd317e4d5
Create Date: 2023-04-02 13:32:34.063024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '865161dee141'
down_revision = 'b7bbd317e4d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rewards',
    sa.Column('rid', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('expire_date', sa.DateTime(), nullable=True),
    sa.Column('users', sa.String(length=550), nullable=True),
    sa.PrimaryKeyConstraint('rid'),
    sa.UniqueConstraint('code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rewards')
    # ### end Alembic commands ###
