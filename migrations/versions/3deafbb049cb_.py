"""empty message

Revision ID: 3deafbb049cb
Revises: 
Create Date: 2019-08-31 00:33:19.752886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3deafbb049cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('username', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('bank_accounts',
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('deposits',
    sa.Column('uuid', sa.String(), nullable=False),
    sa.Column('account_id', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['bank_accounts.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deposits')
    op.drop_table('bank_accounts')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
