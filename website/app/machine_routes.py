from flask import Flask,Blueprint,request,render_template,url_for,abort,flash,redirect
from website.models import db, User, Machine, UserMixin
from wtforms import StringField, validators, TextAreaField, DateField, IntegerField, FileField
from flask_wtf import FlaskForm
from flask_mail import Message
from website import mail, limiter
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import base64




# creating blueprint for machine routes
machine_routes = Blueprint("machine_routes", __name__)



# to generate decoder for image being saved on the database
@machine_routes.app_template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')


# the route to display all machine in the user's database
@machine_routes.route("/machines", methods=["GET"])
@limiter.limit("10/minute") 
@login_required
def machines():
    # Retrieve machines from the database
    machines = Machine.query.filter_by(user_id=current_user.id).all()
    return render_template("machines.html", machines=machines, user=current_user)


#form for add new machine to the user's database.
class Addmachine(FlaskForm):
    machine_name = StringField("Machine Name", [validators.DataRequired("Machine name is required")])
    machine_model = StringField("Machine Model", [validators.DataRequired("Machine Model is required")])
    machine_serial_number = StringField("Machine Serial Number", [validators.DataRequired("Machine serial number is required")])
    machine_manufacturer = StringField("Machine Manufacturer", [validators.DataRequired("Machine manufacturer is required")])
    machine_location = StringField("Machine Location", [validators.DataRequired("Machine location is required")])
    machine_warranty_expiration_date = DateField("Machine Warranty Expire Date")
    machine_purchase_date = DateField("Machine Purchase Date", [validators.DataRequired("Machine purchase date is required")])
    machine_operational_hours = IntegerField("Machine Operational Hours")
    machine_error_logs = TextAreaField("Machine Error Log")
    machine_description = TextAreaField("Machine Description")
    machine_images = FileField("Machine Image", [validators.DataRequired("Machine image is required")])



#the route to add a new machine to the user's database
@machine_routes.route("/add_machine", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def add_machine():

    form = Addmachine()
    if form.validate_on_submit():
        machine_name = form.machine_name.data
        machine_model = form.machine_model.data
        machine_serial_number = form.machine_serial_number.data
        machine_manufacturer = form.machine_manufacturer.data
        machine_location = form.machine_location.data
        machine_warranty_expiration_date = form.machine_warranty_expiration_date.data
        machine_purchase_date = form.machine_purchase_date.data
        machine_operational_hours = form.machine_operational_hours.data
        machine_error_logs = form.machine_error_logs.data
        machine_description = form.machine_description.data
        machine_images = form.machine_images.data
    
        # Save the machine to the database
        new_machine = Machine(
            machine_name=machine_name,
            machine_model=machine_model,
            machine_serial_number=machine_serial_number,
            machine_manufacturer=machine_manufacturer,
            machine_location=machine_location,
            machine_warranty_expiration_date=machine_warranty_expiration_date,
            machine_purchase_date=machine_purchase_date,
            machine_operational_hours=machine_operational_hours,
            machine_error_logs=machine_error_logs,
            machine_description=machine_description,
            machine_images=machine_images.read(),
            user_id=current_user.id
        )
        db.session.add(new_machine)
        db.session.commit()

        # Redirect to the machines page to machines page
        return redirect(url_for("machine_routes.machines"))  

    return render_template("add_machine.html", form=form, user=current_user)



# route to display a machine using it's serial number
@machine_routes.route("/machine", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def one_machine():

    if request.method == "POST":
        machine_serial_number = request.form.get("machine_serial_number")

        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number).first_or_404()

        return render_template("one_machine.html", machine=machine, user=current_user)

    return render_template("search_form_onemachine.html")


#form for edit a machine to the user's database.
class Editmachine(FlaskForm):

    machine_operational_hours = IntegerField("Machine Operational Hours")
    machine_error_logs = TextAreaField("Machine Error Log")
    machine_description = TextAreaField("Machine Description")


#route to edit a machine from the user's database
@machine_routes.route("/machine/update/<string:machine_serial_number>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def update_machine(machine_serial_number):
    
    machine = Machine.query.filter_by(machine_serial_number=machine_serial_number).first_or_404()

    form = Editmachine(obj=machine)

    if form.validate_on_submit():
        machine.machine_error_logs = form.machine_error_logs.data
        machine.machine_description = form.machine_description.data
        machine.date_updated = datetime.utcnow()
        db.session.commit()

        
        return redirect(url_for("machine_routes.machines"))
    
    return render_template("edit_machine.html", form=form,  machine=machine, machine_serial_number=machine_serial_number, user=current_user)


#route to delete a machine from the user's database
@machine_routes.route("/machine/delete/<string:machine_serial_number>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def delete_machine(machine_serial_number):

    machine = Machine.query.filter_by(machine_serial_number=machine_serial_number).first_or_404()
  
    if request.method == "POST":
        db.session.delete(machine)
        db.session.commit()

        return redirect(url_for('machine_routes.machines'))

    return render_template("delete_machine.html", machine=machine, machine_serial_number=machine_serial_number, user=current_user)
    
    
