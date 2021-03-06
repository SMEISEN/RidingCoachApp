"""remove tire pressure

Revision ID: e109041b33dd
Revises: c6ea7844c8b9
Create Date: 2020-12-29 11:55:57.930695

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e109041b33dd'
down_revision = 'c6ea7844c8b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bike', 'slick_rear_pressure')
    op.drop_column('bike', 'rain_front_pressure')
    op.drop_column('bike', 'rain_rear_pressure')
    op.drop_column('bike', 'slick_front_pressure')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bike', sa.Column('slick_front_pressure', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('bike', sa.Column('rain_rear_pressure', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('bike', sa.Column('rain_front_pressure', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('bike', sa.Column('slick_rear_pressure', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
