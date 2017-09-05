"""empty message

Revision ID: 97e60ea2bf99
Revises: 8f60e2552f8d
Create Date: 2017-09-04 19:20:17.763442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97e60ea2bf99'
down_revision = '8f60e2552f8d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('instance', sa.Column('ip', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('instance', 'ip')
    # ### end Alembic commands ###
