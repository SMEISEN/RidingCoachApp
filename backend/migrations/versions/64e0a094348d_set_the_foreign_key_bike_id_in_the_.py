"""Set the foreign key bike id in the maintenance model to be not nullable

Revision ID: 64e0a094348d
Revises: 75d584ca4e5d
Create Date: 2020-11-14 22:57:35.566324

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '64e0a094348d'
down_revision = '75d584ca4e5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('maintenance', 'bike_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('maintenance', 'bike_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    # ### end Alembic commands ###