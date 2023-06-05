from flask import Flask,Blueprint,request,render_template,url_for,abort,flash,redirect
from website.models import db, User, Machine, UserMixin, MachineMaintenanceReport, MaintenanceSchedule
from wtforms import StringField, validators, TextAreaField, DateField, EmailField, DecimalField,DateTimeField
from flask_wtf import FlaskForm
from flask_mail import Message
from website import mail, limiter
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime



# creating blueprint for maintenance schedule routes
maintenance_schedule = Blueprint("maintenance_schedule", __name__)



# route to display all maintenace schedules
@maintenance_schedule.route("/all_maintenance_schedules", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def all_maintenance_schedules():
    
    if request.method == "POST":
        machine_serial_number = request.form.get("machine_serial_number")
        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number, user_id=current_user.id).first_or_404()
    
        all_maintenance_schedules = MaintenanceSchedule.query.filter_by(machine_id=machine.id, user_id=current_user.id).all()
        return render_template("all_maintenance_schedule.html", machine=machine, 
                           user=current_user, all_maintenance_schedules=all_maintenance_schedules, 
                           machine_serial_number=machine_serial_number)
    
    return render_template("search_form_maintenance_schedule.html")


class AddMaintenanceScheduleForm(FlaskForm):
    technician_name = StringField("Technician Name")
    schedule_tasks = TextAreaField("Schedule Tasks")
    schedule_date = DateField("Schedule Date", [validators.DataRequired("Schedule date is required")])
    notes = TextAreaField("Notes")
    status = StringField("Status", [validators.DataRequired("Status is required")])
    


#route to add a new maintenance schedule
@maintenance_schedule.route("/add_schedule/<string:machine_serial_number>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def add_schedule(machine_serial_number):
    form = AddMaintenanceScheduleForm()
    if form.validate_on_submit():
        technician_name = form.technician_name.data
        schedule_tasks = form.schedule_tasks.data
        schedule_date = form.schedule_date.data
        notes = form.notes.data
        status = form.status.data
        
       

        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number).first_or_404()
       

        new_schedule = MaintenanceSchedule(schedule_date=schedule_date,status=status,schedule_tasks=schedule_tasks,notes=notes,
                                           technician_name=technician_name,user_id=current_user.id, machine_id=machine.id)
        db.session.add(new_schedule)
        db.session.commit()

        return redirect(url_for("maintenance_schedule.all_maintenance_schedules"))
    
    return render_template("add_schedule.html", machine_serial_number=machine_serial_number, form=form, user=current_user)



class SearcMaintenanceScheduleForm(FlaskForm):
    schedule_date = DateField("Schedule Date", [validators.DataRequired("Schedule date is required")])
    
#route to get and display maintenance schedule based on the schedule date
#route to get and display maintenance schedule based on the schedule date
@maintenance_schedule.route("/all_maintenance_schedules_by_schedule_date/<string:machine_serial_number>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def all_maintenance_schedules_by_schedule_date(machine_serial_number):
    form = SearcMaintenanceScheduleForm()
    if form.validate_on_submit():
        schedule_date = form.schedule_date.data
       
        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number, user_id=current_user.id).first()
        all_maintenance_schedules_by_schedule_date = MaintenanceSchedule.query.filter_by(machine_id=machine.id, 
                                                                            schedule_date=schedule_date).all()
        print("All maintenance schedules:", all_maintenance_schedules_by_schedule_date)

        return render_template("all_maintenance_schedule.html", user=current_user,
                               machine_serial_number=machine_serial_number,
                               all_maintenance_schedules=all_maintenance_schedules_by_schedule_date, machine=machine)

   
    return render_template("maintenance_schedule_date.html", machine_serial_number=machine_serial_number, form=form)


#form for edit a maintenance schedule to the user's database.
class EditMaintenanceSchedule(FlaskForm):

    schedule_date = DateTimeField("Schedule Date", [validators.DataRequired("Schedule date is required")])
    notes = TextAreaField("Notes")
    schedule_tasks = TextAreaField("Schedule Tasks")
    status = StringField("Status", [validators.DataRequired("Status is required")])
    technician_name = StringField("Technician Name")



# Route to edit the maintenance schedule
@maintenance_schedule.route("/edit-maintenance-schedule/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def edit_maintenance_schedule(id):
    schedule = MaintenanceSchedule.query.get_or_404(id)
    form = EditMaintenanceSchedule(obj=schedule)

    if form.validate_on_submit():
        schedule.schedule_date = form.schedule_date.data
        schedule.status = form.status.data
        schedule.schedule_tasks = form.schedule_tasks.data
        schedule.notes = form.notes.data
        schedule.technician_name = form.technician_name.data

        db.session.commit()
        return redirect(url_for("maintenance_schedule.all_maintenance_schedules"))

    return render_template("edit_maintenance_schedule.html", form=form, schedule=schedule)


# Route to delete the maintenance schedule
@maintenance_schedule.route("/delete-maintenance-schedule/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def delete_maintenance_schedule(id):

    schedule = MaintenanceSchedule.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(schedule)
        db.session.commit()
        return redirect(url_for("maintenance_schedule.all_maintenance_schedules"))
    
    return render_template("delete_maintenance_schedule.html", schedule=schedule)


# # Define the RecipientEmailForm
class RecipientEmailForm(FlaskForm):
    recipient = EmailField('Recipient Email', [validators.DataRequired("Recipient email address is required")])
    

# Route to send maintenance notification email
@maintenance_schedule.route("/send_maintenance_schedule_email/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def send_maintenance_schedule_email(id):
    schedule = MaintenanceSchedule.query.get_or_404(id)

    form = RecipientEmailForm()

    if form.validate_on_submit():
        recipient = form.recipient.data

        # Send email schedule
        send_email_schedule(schedule, recipient)

        return redirect(url_for("maintenance_schedule.all_maintenance_schedules"))

    return render_template("recipient_email_form_schedule.html", form=form, schedule=schedule)

#function to send notification to email
def send_email_schedule(schedule, recipient):
    subject = "Maintenance Schedule"
    sender = "abiolaadedayo1993@gmail.com"

    machine= Machine.query.filter_by(user_id=current_user.id).first_or_404()

    # Create the email message
    message = Message(subject, sender=sender, recipients=[recipient])
    message.html = render_template("email_template_schedule.html", schedule=schedule, recipient=recipient, machine=machine)

    # Send the email
    mail.send(message)