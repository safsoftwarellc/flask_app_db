"""message db tables created

Revision ID: c06382624e03
Revises: 6fb7aed622a0
Create Date: 2022-03-07 23:25:05.570021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c06382624e03'
down_revision = '6fb7aed622a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_data',
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=50), nullable=False),
    sa.Column('file_data', sa.LargeBinary(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('file_id'),
    sa.UniqueConstraint('file_name')
    )
    op.create_table('message_text_data',
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=50), nullable=False),
    sa.Column('header_text', sa.String(length=600), nullable=True),
    sa.Column('footer_text', sa.String(length=600), nullable=True),
    sa.Column('line_1', sa.String(length=600), nullable=True),
    sa.Column('line_2', sa.String(length=600), nullable=True),
    sa.Column('line_3', sa.String(length=600), nullable=True),
    sa.Column('line_4', sa.String(length=600), nullable=True),
    sa.Column('line_5', sa.String(length=600), nullable=True),
    sa.Column('line_6', sa.String(length=600), nullable=True),
    sa.Column('line_7', sa.String(length=600), nullable=True),
    sa.Column('line_8', sa.String(length=600), nullable=True),
    sa.Column('line_9', sa.String(length=600), nullable=True),
    sa.Column('line_10', sa.String(length=600), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('file_id'),
    sa.UniqueConstraint('file_name')
    )
   
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    
    op.drop_table('message_text_data')
    op.drop_table('message_data')
    # ### end Alembic commands ###
