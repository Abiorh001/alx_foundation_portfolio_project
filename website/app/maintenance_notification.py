from flask import Flask,Blueprint,request,render_template,url_for,abort,flash,redirect
from website.models import db, User, Machine, MaintenanceNotification
from wtforms import StringField, validators, TextAreaField, DateField, IntegerField, FileField, DecimalField, EmailField
from flask_wtf import FlaskForm
from flask_mail import Message
from website import mail, limiter
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime



# creating blueprint for  maintenance report notification routes
maintenance_notification = Blueprint("maintenance_notification", __name__)



# route to display all maintenace report notification 
@maintenance_notification.route("/all_maintenance_notifications", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def all_maintenance_notifications():
    
    if request.method == "POST":
        machine_serial_number = request.form.get("machine_serial_number")
        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number, user_id=current_user.id).first_or_404()
    
        all_maintenance_notifications = MaintenanceNotification.query.filter_by(machine_id=machine.id, user_id=current_user.id).all()
        return render_template("all_maintenance_notifications.html", machine=machine, 
                           user=current_user, all_maintenance_notifications=all_maintenance_notifications, 
                           machine_serial_number=machine_serial_number)
    
    return render_template("search_form_maintenance_notification.html")


#form for add new machine to the user's database.
class AddMaintenanceNotification(FlaskForm):
    description = TextAreaField("Notification Description", [validators.DataRequired("Notification description problem is required")])
    status = StringField("Status", [validators.DataRequired("Status is required")])
    notification_datetime  =DateField("Notification Date", [validators.DataRequired("Notification date is required")])


@maintenance_notification.route("/add_notification/<string:machine_serial_number>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def add_notification(machine_serial_number):
    form = AddMaintenanceNotification()
    if form.validate_on_submit():
        description = form.description.data
        status = form.status.data
        notification_datetime = form.notification_datetime.data
        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number).first_or_404()
       

        new_notification = MaintenanceNotification(description=description, status=status, notification_datetime=notification_datetime,
                                                         user_id=current_user.id, machine_id=machine.id)
        db.session.add(new_notification)
        db.session.commit()

        return redirect(url_for("maintenance_notification.all_maintenance_notifications"))
    
    return render_template("add_notification.html", machine_serial_number=machine_serial_number, form=form, user=current_user)


#route to get and display maintenance notification based on the report date
@maintenance_notification.route("/all_maintenance_notifications-report_date/<string:machine_serial_number>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def all_maintenance_notification_by_report_date(machine_serial_number):
    if request.method == "POST":

        notification_datetime = request.form.get("notification_datetime")
        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number, user_id=current_user.id).first()
        all_maintenance_notification_by_report_date = MaintenanceNotification.query.filter_by(machine_id=machine.id, 
                                                                            notification_datetime=notification_datetime).all()

        return render_template("all_maintenance_notifications.html", user=current_user,
                               machine_serial_number=machine_serial_number,
                               all_maintenance_notifications=all_maintenance_notification_by_report_date, machine=machine)

    return render_template("maintenance_notification_date.html", machine_serial_number=machine_serial_number)



#form for edit a maintenance reports to the user's database.
class EditMaintenanceNotification(FlaskForm):

    description = TextAreaField("Notification Description")
    status = StringField("Status")
    notification_datetime  =DateField("Notification Date")



# Route to edit the maintenance notification
@maintenance_notification.route("/edit-maintenance-notification/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def edit_maintenance_notification(id):
    notification = MaintenanceNotification.query.get_or_404(id)
    form = EditMaintenanceNotification(obj=notification)

    if form.validate_on_submit():
        notification.description = form.description.data
        notification.status = form.status.data
        notification.notification_datetime = form.notification_datetime.data

        db.session.commit()
        return redirect(url_for("maintenance_notification.all_maintenance_notifications"))

    return render_template("edit_maintenance_notification.html", form=form, notification=notification)


# Route to delete the maintenance notification
@maintenance_notification.route("/delete-maintenance-notification/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def delete_maintenance_notification(id):

    notification = MaintenanceNotification.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(notification)
        db.session.commit()
        return redirect(url_for("maintenance_notification.all_maintenance_notifications"))
    
    return render_template("delete_maintenance_notification.html", notification=notification)


# Define the RecipientEmailForm
class RecipientEmailForm(FlaskForm):
    recipient = EmailField('Recipient Email', [validators.DataRequired("Recipient email address is required")])
    

# Route to send maintenance notification email
@maintenance_notification.route("/send_maintenance_notification_email/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def send_maintenance_notification_email(id):
    notification = MaintenanceNotification.query.get_or_404(id)

    form = RecipientEmailForm()

    if form.validate_on_submit():
        recipient = form.recipient.data

        # Send email notification
        send_email_notification(notification, recipient)

        return redirect(url_for("maintenance_notification.all_maintenance_notifications"))

    return render_template("recipient_email_form.html", form=form, notification=notification)

#function to send notification to email
def send_email_notification(notification, recipient):
    subject = "Maintenance Notification"
    sender = "abiolaadedayo1993@gmail.com"

    machine= Machine.query.filter_by(user_id=current_user.id).first_or_404()

    # Create the email message
    message = Message(subject, sender=sender, recipients=[recipient])
    message.html = render_template("email_template.html", notification=notification, recipient=recipient, machine=machine)

    # Send the email
    mail.send(message)