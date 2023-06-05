from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime
import uuid



# creating an instance of database
db = SQLAlchemy()

# Table schema for User
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150))
    phone_number = db.Column(db.String(150))
    email_address = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    street_address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    zip_code = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(150), nullable=False)
    reset_token = db.Column(db.String(128), default=None)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)

    machines = db.relationship('Machine', backref='user', lazy='dynamic', cascade="delete")
    machine_maintenance_reports = db.relationship('MachineMaintenanceReport', backref='user', lazy='dynamic', cascade='delete')
    maintenance_report_notifications = db.relationship('MaintenanceNotification', backref='user', lazy='dynamic', cascade='delete')
    maintenance_schedule = db.relationship('MaintenanceSchedule', backref='user', lazy='dynamic', cascade='delete')


class Machine(db.Model, UserMixin):
    __tablename__ = 'machine'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    machine_name = db.Column(db.String(150), nullable=False)
    machine_model = db.Column(db.String(150), nullable=False)
    machine_serial_number = db.Column(db.String(150), nullable=False)
    machine_manufacturer = db.Column(db.String(150), nullable=False)
    machine_location = db.Column(db.String(150), nullable=False)
    machine_warranty_expiration_date = db.Column(db.Date)
    machine_purchase_date = db.Column(db.Date)
    machine_operational_hours = db.Column(db.Integer)
    machine_error_logs = db.Column(db.Text)
    machine_description = db.Column(db.Text)
    machine_images = db.Column(db.LargeBinary)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)

    machine_maintenance_reports = db.relationship('MachineMaintenanceReport', backref='machine', lazy='dynamic', cascade='delete')
    maintenance_report_notifications = db.relationship('MaintenanceNotification', backref='machine', lazy='dynamic', cascade='delete')
    maintenance_schedule = db.relationship('MaintenanceSchedule', backref='machine',lazy='dynamic', cascade='delete')


class MachineMaintenanceReport(db.Model, UserMixin):
    __tablename__ = "machine_maintenance_report"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    maintenance_task_problem = db.Column(db.Text, nullable=False)
    technician_name = db.Column(db.String(150), nullable=False)
    maintenance_type = db.Column(db.String(150), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    maintenance_task_solution = db.Column(db.Text)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    labor_hours = db.Column(db.DECIMAL(10, 2))
    parts_cost = db.Column(db.DECIMAL(10, 2))
    additional_notes = db.Column(db.Text)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    machine_id = db.Column(db.String(36), db.ForeignKey('machine.id'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
   


class MaintenanceNotification(db.Model, UserMixin):
    __tablename__ = 'maintenance_notification'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(150), nullable=False)
    notification_datetime = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    machine_id = db.Column(db.String(36), db.ForeignKey('machine.id'))
  


class MaintenanceSchedule(db.Model, UserMixin):
    __tablename__ = 'maintenance_schedule'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    schedule_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    machine_id = db.Column(db.String(36), db.ForeignKey('machine.id'))
    schedule_tasks = db.Column(db.Text)
    status = db.Column(db.String(150), nullable=False)
    technician_name = db.Column(db.String(150))



# Table schema for Workload
class Workload(db.Model, UserMixin):

    __tablename__ = "workload"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    machine_id = db.Column(db.String(36), db.ForeignKey('machine.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    assigned_technician = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow)



#Table schema for contact us
class Contacts(db.Model,UserMixin):

    __tablename__ = "contacts"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    message = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    

