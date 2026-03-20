"""add user_id to pets and drop owners tables

Revision ID: a1b2c3d4e5f6
Revises: eff3d497b8f2
Create Date: 2026-03-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'eff3d497b8f2'
branch_labels = None
depends_on = None


def upgrade():
    # Drop junction table first (depends on pets and owners)
    op.drop_table('pet_owner')

    # Drop owners table
    op.drop_table('owners')

    # Add user_id column to pets (FK to users.id)
    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('pets_user_id_fkey', 'users', ['user_id'], ['id'])

    # Make user_id NOT NULL (safe if DB is empty; if there's data, update first)
    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.Integer(), nullable=False)


def downgrade():
    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.drop_constraint('pets_user_id_fkey', type_='foreignkey')
        batch_op.drop_column('user_id')

    op.create_table('owners',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('address', sa.String(length=125), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    op.create_table('pet_owner',
        sa.Column('pet_id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['owners.id'], ),
        sa.ForeignKeyConstraint(['pet_id'], ['pets.id'], ),
        sa.PrimaryKeyConstraint('pet_id', 'owner_id')
    )
