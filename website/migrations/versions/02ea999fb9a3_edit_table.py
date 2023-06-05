"""edit table

Revision ID: 02ea999fb9a3
Revises: f054190dca5c
Create Date: 2023-05-26 04:41:52.212993

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '02ea999fb9a3'
down_revision = 'f054190dca5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('maintenance_report_notification', schema=None) as batch_op:
        batch_op.drop_constraint('maintenance_report_notification_ibfk_1', type_='foreignkey')
        batch_op.drop_column('machine_maintenance_report_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('maintenance_report_notification', schema=None) as batch_op:
        batch_op.add_column(sa.Column('machine_maintenance_report_id', mysql.VARCHAR(length=36), nullable=True))
        batch_op.create_foreign_key('maintenance_report_notification_ibfk_1', 'machine_maintenance_report', ['machine_maintenance_report_id'], ['id'])

    # ### end Alembic commands ###
