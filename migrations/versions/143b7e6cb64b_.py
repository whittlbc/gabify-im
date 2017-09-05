"""empty message

Revision ID: 143b7e6cb64b
Revises: 
Create Date: 2017-09-04 14:54:17.164032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '143b7e6cb64b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.String(length=120), nullable=False),
    sa.Column('repo', sa.String(length=240), nullable=True),
    sa.Column('is_destroyed', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_uid'), 'project', ['uid'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_uid'), table_name='project')
    op.drop_table('project')
    # ### end Alembic commands ###