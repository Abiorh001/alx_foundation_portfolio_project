from flask import Flask,Blueprint,request,render_template,url_for,abort,flash,redirect
from website.models import db, User, Contacts
from wtforms import StringField, PasswordField, validators, EmailField
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from website import mail
import secrets
from flask_login import login_user, login_required, logout_user, current_user








# creating blueprint for authentication routes
views= Blueprint("views", __name__ )


@views.route("/")
def home():
    return render_template("landing_page.html")


# Route for saving contact us information
@views.route("/contacts", methods=['GET', 'POST'])
def contacts():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        contact = Contacts(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()

        return redirect(url_for("views.home"))
    return render_template("contact.html")


@views.route("/services")
def services():
    return render_template("services.html")

@views.route("/aboutus")
def about_us():
    return render_template("about_us.html")