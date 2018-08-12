""" menambahkan kolom dari pada table rute

Revision ID: 5d138f07c36b
Revises: 0226430981fb
Create Date: 2018-08-11 11:27:40.399640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d138f07c36b'
down_revision = '0226430981fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rute', sa.Column('dari', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rute', 'dari')
    # ### end Alembic commands ###