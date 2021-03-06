"""added datetime created and modified to all models and changed name of weather column in the setup and training model to prevent confusion

Revision ID: 8bbf445aad7c
Revises: dd0739079388
Create Date: 2020-07-06 11:44:40.246950

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8bbf445aad7c'
down_revision = 'dd0739079388'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bike', sa.Column('datetime_created', sa.DateTime(), nullable=True))
    op.add_column('bike', sa.Column('datetime_last_modified', sa.DateTime(), nullable=True))
    op.add_column('maintenance', sa.Column('datetime_created', sa.DateTime(), nullable=True))
    op.add_column('maintenance', sa.Column('datetime_last_modified', sa.DateTime(), nullable=True))
    op.add_column('setup', sa.Column('weather_current', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.drop_column('setup', 'weather')
    op.add_column('training', sa.Column('weather_hourly', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.drop_column('training', 'weather')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('training', sa.Column('weather', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False))
    op.drop_column('training', 'weather_hourly')
    op.add_column('setup', sa.Column('weather', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.drop_column('setup', 'weather_current')
    op.drop_column('maintenance', 'datetime_last_modified')
    op.drop_column('maintenance', 'datetime_created')
    op.drop_column('bike', 'datetime_last_modified')
    op.drop_column('bike', 'datetime_created')
    # ### end Alembic commands ###
