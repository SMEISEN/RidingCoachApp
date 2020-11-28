"""added sparepart and sparepartitem table

Revision ID: 6239355ee47c
Revises: 64e0a094348d
Create Date: 2020-11-28 19:49:09.421909

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6239355ee47c'
down_revision = '64e0a094348d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sparepart',
    sa.Column('sparepart_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('module', sa.String(), nullable=False),
    sa.Column('min_stock', sa.Integer(), nullable=True),
    sa.Column('datetime_created', sa.DateTime(), nullable=False),
    sa.Column('datetime_last_modified', sa.DateTime(), nullable=False),
    sa.Column('datetime_display', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('sparepart_id'),
    sa.UniqueConstraint('sparepart_id')
    )
    op.create_table('sparepartitem',
    sa.Column('sparepartitem_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('sparepart_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('condition', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('datetime_created', sa.DateTime(), nullable=False),
    sa.Column('datetime_last_modified', sa.DateTime(), nullable=False),
    sa.Column('datetime_display', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['sparepart_id'], ['sparepart.sparepart_id'], ),
    sa.PrimaryKeyConstraint('sparepartitem_id'),
    sa.UniqueConstraint('sparepartitem_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sparepartitem')
    op.drop_table('sparepart')
    # ### end Alembic commands ###
