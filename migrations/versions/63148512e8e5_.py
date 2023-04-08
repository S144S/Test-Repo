"""empty message

Revision ID: 63148512e8e5
Revises: 3b9dac2ea5aa
Create Date: 2023-04-08 16:22:12.182024

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63148512e8e5'
down_revision = '3b9dac2ea5aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('position', sa.String(length=500), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.drop_column('position')

    # ### end Alembic commands ###
