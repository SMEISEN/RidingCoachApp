"""extended bike table, added columns for tire pressure recommendation and application notes

Revision ID: 34fffdb29082
Revises: 0e33b088ff70
Create Date: 2020-08-04 12:11:36.415282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34fffdb29082'
down_revision = '0e33b088ff70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bike', sa.Column('rain_front_name', sa.String(length=50), nullable=True))
    op.add_column('bike', sa.Column('rain_front_pressure_base', sa.Float(), nullable=True))
    op.add_column('bike', sa.Column('rain_front_pressure_notes', sa.Text(), nullable=True))
    op.add_column('bike', sa.Column('rain_rear_name', sa.String(length=50), nullable=True))
    op.add_column('bike', sa.Column('rain_rear_pressure_base', sa.Float(), nullable=True))
    op.add_column('bike', sa.Column('rain_rear_pressure_notes', sa.Text(), nullable=True))
    op.add_column('bike', sa.Column('slick_front_name', sa.String(length=50), nullable=True))
    op.add_column('bike', sa.Column('slick_front_pressure_base', sa.Float(), nullable=True))
    op.add_column('bike', sa.Column('slick_front_pressure_notes', sa.Text(), nullable=True))
    op.add_column('bike', sa.Column('slick_rear_name', sa.String(length=50), nullable=True))
    op.add_column('bike', sa.Column('slick_rear_pressure_base', sa.Float(), nullable=True))
    op.add_column('bike', sa.Column('slick_rear_pressure_notes', sa.Text(), nullable=True))
    op.drop_column('bike', 'slick_front')
    op.drop_column('bike', 'rain_front')
    op.drop_column('bike', 'rain_rear')
    op.drop_column('bike', 'slick_rear')
    op.create_unique_constraint(None, 'coach', ['coach_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'coach', type_='unique')
    op.add_column('bike', sa.Column('slick_rear', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('bike', sa.Column('rain_rear', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('bike', sa.Column('rain_front', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.add_column('bike', sa.Column('slick_front', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('bike', 'slick_rear_pressure_notes')
    op.drop_column('bike', 'slick_rear_pressure_base')
    op.drop_column('bike', 'slick_rear_name')
    op.drop_column('bike', 'slick_front_pressure_notes')
    op.drop_column('bike', 'slick_front_pressure_base')
    op.drop_column('bike', 'slick_front_name')
    op.drop_column('bike', 'rain_rear_pressure_notes')
    op.drop_column('bike', 'rain_rear_pressure_base')
    op.drop_column('bike', 'rain_rear_name')
    op.drop_column('bike', 'rain_front_pressure_notes')
    op.drop_column('bike', 'rain_front_pressure_base')
    op.drop_column('bike', 'rain_front_name')
    # ### end Alembic commands ###
