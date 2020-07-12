"""Changed datetime colums to be not nullable

Revision ID: 41d9e0fd5fbd
Revises: 8bbf445aad7c
Create Date: 2020-07-12 10:53:23.608127

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '41d9e0fd5fbd'
down_revision = '8bbf445aad7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bike', 'datetime_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('bike', 'datetime_last_modified',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('maintenance', 'datetime_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('maintenance', 'datetime_last_modified',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('maintenance', 'datetime_last_modified',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('maintenance', 'datetime_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('bike', 'datetime_last_modified',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('bike', 'datetime_created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
