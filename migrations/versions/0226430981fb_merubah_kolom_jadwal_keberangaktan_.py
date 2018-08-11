"""merubah kolom jadwal keberangaktan dengan tanggal_keberangkatan

Revision ID: 0226430981fb
Revises: 0c85d27da92e
Create Date: 2018-08-11 07:31:59.195316

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0226430981fb'
down_revision = '0c85d27da92e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rute', sa.Column('tanggal_keberangkatan', sa.Date(), nullable=True))
    op.drop_column('rute', 'jadwal_keberangkatan')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rute', sa.Column('jadwal_keberangkatan', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('rute', 'tanggal_keberangkatan')
    # ### end Alembic commands ###
