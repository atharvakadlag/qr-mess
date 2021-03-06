"""empty message

Revision ID: 90c8e58ef6d8
Revises: 
Create Date: 2022-01-12 22:58:52.255009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90c8e58ef6d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('main',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('current_time', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('slot', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'name', 'slot', name='_entry_uc')
    )
    op.create_index(op.f('ix_main_name'), 'main', ['name'], unique=False)
    op.create_index(op.f('ix_main_slot'), 'main', ['slot'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_main_slot'), table_name='main')
    op.drop_index(op.f('ix_main_name'), table_name='main')
    op.drop_table('main')
    # ### end Alembic commands ###
