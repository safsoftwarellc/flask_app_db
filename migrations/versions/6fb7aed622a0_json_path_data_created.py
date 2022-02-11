"""json_path_data created

Revision ID: 6fb7aed622a0
Revises: 21071863d330
Create Date: 2022-02-11 06:26:31.099531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fb7aed622a0'
down_revision = '21071863d330'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('json_path_excel_sheet_mapping',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('json_file_name', sa.String(length=100), nullable=False),
    sa.Column('json_path_name', sa.String(length=50), nullable=False),
    sa.Column('json_path_string', sa.String(length=250), nullable=False),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('json_path_excel_sheet_mapping')
    # ### end Alembic commands ###
