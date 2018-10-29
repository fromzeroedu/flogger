"""empty message

Revision ID: 9a0c0a72899e
Revises: 776a6026caf2
Create Date: 2018-10-22 14:23:40.562347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a0c0a72899e'
down_revision = '776a6026caf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image', sa.String(length=36), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image')
    # ### end Alembic commands ###