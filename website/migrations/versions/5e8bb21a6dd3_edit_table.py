"""edit table

Revision ID: 5e8bb21a6dd3
Revises: 02ea999fb9a3
Create Date: 2023-05-26 09:04:38.851090

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5e8bb21a6dd3'
down_revision = '02ea999fb9a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('maintenance_report_notification', schema=None) as batch_op:
        batch_op.drop_index('id')

    op.drop_table('maintenance_report_notification')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('maintenance_report_notification',
    sa.Column('id', mysql.VARCHAR(length=36), nullable=False),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('status', mysql.VARCHAR(length=150), nullable=False),
    sa.Column('notification_datetime', mysql.DATETIME(), nullable=True),
    sa.Column('date_created', mysql.DATETIME(), nullable=True),
    sa.Column('date_updated', mysql.DATETIME(), nullable=True),
    sa.Column('user_id', mysql.VARCHAR(length=36), nullable=True),
    sa.Column('machine_id', mysql.VARCHAR(length=36), nullable=True),
    sa.ForeignKeyConstraint(['machine_id'], ['machine.id'], name='maintenance_report_notification_ibfk_3'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='maintenance_report_notification_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('maintenance_report_notification', schema=None) as batch_op:
        batch_op.create_index('id', ['id'], unique=False)

    # ### end Alembic commands ###
