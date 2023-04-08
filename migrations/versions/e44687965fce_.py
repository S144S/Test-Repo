"""empty message

Revision ID: e44687965fce
Revises: dedfed553821
Create Date: 2023-04-06 18:39:05.257278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e44687965fce'
down_revision = 'dedfed553821'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('groups', schema=None) as batch_op:
        batch_op.drop_column('avatar')

    # ### end Alembic commands ###
