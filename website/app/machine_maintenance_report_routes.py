from flask import Flask,Blueprint,request,render_template,url_for,abort,flash,redirect
from website.models import db, User, Machine, UserMixin, MachineMaintenanceReport
from wtforms import StringField, validators, TextAreaField, DateField, IntegerField, FileField, DecimalField
from flask_wtf import FlaskForm
from flask_mail import Message
from website import mail, limiter
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime



# creating blueprint for machine maintenance reports routes
machine_maintenance_report_routes = Blueprint("machine_maintenance_report_routes", __name__)


#the route that display all machine maintenance reports using it's serial number
@machine_maintenance_report_routes.route("/all-maintenance-reports", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def all_maintenance_reports():
    
    if request.method == "POST":
        machine_serial_number = request.form.get("machine_serial_number")
        user_id = current_user.id
        machine = Machine.query.filter_by(user_id=user_id, machine_serial_number=machine_serial_number).first_or_404()
        all_maintenance_reports = MachineMaintenanceReport.query.filter_by(machine_id=machine.id, user_id=user_id).all()
        return render_template("all_machine_maintenance_reports.html", machine=machine, 
                           user=current_user, all_maintenance_reports=all_maintenance_reports, machine_serial_number=machine_serial_number)
    return render_template("search_form_maintenance.html")


#form for add new machine to the user's database.
class AddMaintenanceReport(FlaskForm):
    maintenance_task_problem = TextAreaField("Maintenance Task Problem", [validators.DataRequired("Maintenance task problem is required")])
    technician_name = StringField("Technician Name", [validators.DataRequired("Technician Name is required")])
    maintenance_type = StringField("Maintenance Type", [validators.DataRequired("Maintenance Type is required")])
    report_date = DateField("Report Date", [validators.DataRequired("Report date is required")])
    maintenance_task_solution  = TextAreaField("Maintenance Task Solution", [validators.DataRequired("Machine location is required")])
    start_datetime = DateField("Maintenance Start Date", format="%Y-%m-%d")
    end_datetime = DateField("Maintenance End Date", format="%Y-%m-%d")
    labor_hours = IntegerField("Technician Working Hours")
    parts_cost = DecimalField("Maintenance Parts Cost")
    additional_notes = TextAreaField("Maintenance Additional Notes")
   



#the route to add a new maintenance report
@machine_maintenance_report_routes.route("/add-maintenance-report/<string:machine_serial_number>",  methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def add_maintenance_report(machine_serial_number):

    machine = Machine.query.filter_by(machine_serial_number=machine_serial_number).first()
    form = AddMaintenanceReport()

    if form.validate_on_submit():
        maintenance_task_problem = form.maintenance_task_problem.data
        technician_name = form.technician_name.data
        maintenance_type = form.maintenance_type.data
        report_date = form.report_date.data
        maintenance_task_solution = form.maintenance_task_solution.data
        start_datetime = form.start_datetime.data
        end_datetime = form.end_datetime.data
        labor_hours = form.labor_hours.data
        parts_cost = form.parts_cost.data
        additional_notes = form.additional_notes.data

        new_maintenance_report = MachineMaintenanceReport(
            maintenance_task_problem=maintenance_task_problem,
            technician_name=technician_name,
            maintenance_type=maintenance_type,
            report_date=report_date,
            maintenance_task_solution=maintenance_task_solution,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            labor_hours=labor_hours,
            parts_cost=parts_cost,
            additional_notes=additional_notes,
            user_id = current_user.id,
            machine_id = machine.id

        )

        db.session.add(new_maintenance_report)
        db.session.commit()

        return redirect(url_for("machine_maintenance_report_routes.all_maintenance_reports"))
    
    return render_template("add_maintenance_report.html", form=form, user=current_user, machine_serial_number=machine_serial_number)


#route to get and display maintenance reports based on the report date
@machine_maintenance_report_routes.route("/all-maintenance-report_date/<string:machine_serial_number>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def all_maintenance_reports_by_report_date(machine_serial_number):
    if request.method == "POST":

        report_date = request.form.get("report_date")
        machine = Machine.query.filter_by(machine_serial_number=machine_serial_number, user_id=current_user.id).first()
        all_maintenance_reports_by_report_date = MachineMaintenanceReport.query.filter_by(machine_id=machine.id, report_date=report_date).all()

        return render_template("all_machine_maintenance_reports.html", user=current_user,
                               machine_serial_number=machine_serial_number,
                               all_maintenance_reports=all_maintenance_reports_by_report_date, machine=machine)

    return render_template("maintenance_report_date.html", machine_serial_number=machine_serial_number)



#form for edit a maintenance reports to the user's database.
class EditMaintenanceReport(FlaskForm):

    maintenance_task_solution  = TextAreaField("Maintenance Task Solution")
    start_datetime = DateField("Maintenance Start Date", format="%Y-%m-%d")
    end_datetime = DateField("Maintenance End Date", format="%Y-%m-%d")
    labor_hours = IntegerField("Technician Working Hours")
    parts_cost = DecimalField("Maintenance Parts Cost")
    additional_notes = TextAreaField("Maintenance Additional Notes")


# Route to edit the maintenance reports
@machine_maintenance_report_routes.route("/edit-maintenance-report/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def edit_maintenance_report(id):
    maintenance_report = MachineMaintenanceReport.query.get_or_404(id)
    form = EditMaintenanceReport(obj=maintenance_report)

    if form.validate_on_submit():
        maintenance_report.maintenance_task_solution = form.maintenance_task_solution.data
        maintenance_report.start_datetime = form.start_datetime.data
        maintenance_report.end_datetime = form.end_datetime.data
        maintenance_report.labor_hours = form.labor_hours.data
        maintenance_report.parts_cost = form.parts_cost.data
        maintenance_report.additional_notes = form.additional_notes.data

        db.session.commit()
        return redirect(url_for("machine_maintenance_report_routes.all_maintenance_reports"))

    return render_template("edit_maintenance_report.html", form=form, maintenance_report=maintenance_report)


# Route to delete the maintenance reports
@machine_maintenance_report_routes.route("/delete-maintenance-report/<string:id>", methods=["GET", "POST"])
@limiter.limit("10/minute") 
@login_required
def delete_maintenance_report(id):

    maintenance_report = MachineMaintenanceReport.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(maintenance_report)
        db.session.commit()
        return redirect(url_for("machine_maintenance_report_routes.all_maintenance_reports"))
    
    return render_template("delete_maintenance_report.html", maintenance_report=maintenance_report)
