"""excel_sheet_db_table_mapping database migration

Revision ID: 940fa7471ca0
Revises: 8784d98db364
Create Date: 2022-01-03 23:42:45.080211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '940fa7471ca0'
down_revision = '8784d98db364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db_table_excel_sheet_mapping',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('excel_id', sa.Integer(), nullable=False),
    sa.Column('table_mapping', sa.String(length=600), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('excel_id')
    )
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.drop_table('db_table_excel_sheet_mapping')
    # ### end Alembic commands ###