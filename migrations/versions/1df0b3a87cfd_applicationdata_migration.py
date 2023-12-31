"""Applicationdata migration

Revision ID: 1df0b3a87cfd
Revises: 022b22ec6cad
Create Date: 2023-10-02 10:02:19.628557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1df0b3a87cfd'
down_revision = '022b22ec6cad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('relevancyScore', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('isClosed', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('acceptStatus', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('isDeleted', sa.Boolean(), nullable=True))

    with op.batch_alter_table('candidate', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isDeleted', sa.Boolean(), nullable=True))

    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isDeleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.drop_column('isDeleted')

    with op.batch_alter_table('candidate', schema=None) as batch_op:
        batch_op.drop_column('isDeleted')

    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.drop_column('isDeleted')
        batch_op.drop_column('acceptStatus')
        batch_op.drop_column('isClosed')
        batch_op.drop_column('relevancyScore')

    # ### end Alembic commands ###
