from flask import Flask,Blueprint,request,render_template,url_for,abort,flash,redirect
from website.models import db, User
from wtforms import StringField, PasswordField, validators, EmailField
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from website import mail, limiter
import secrets
from flask_login import login_user, login_required, logout_user, current_user






# creating blueprint for authentication routes
auth_routes = Blueprint("auth_routes", __name__)


# creating form class meta data
class SignupForm(FlaskForm):
    """ form class for sign up data"""

    first_name = StringField("First Name", [validators.DataRequired(message="First name is required"),
                                            validators.Length(min=2, max=100)])
    last_name = StringField("Last Name", [validators.Length(min=2, max=100)])
    phone_number= StringField("Phone Number", [validators.Length(min=10, max=100)])
    email_address = EmailField("Email Address", [validators.DataRequired(message="Email address is required"),
                                            validators.Length(min=6, max=100)])
    password = PasswordField('New Password', [validators.DataRequired(message="Password is required"),
                                              validators.EqualTo('confirm', message='Passwords must match'),
                                              validators.Length(min=8, max=100)])
    confirm = PasswordField('Repeat Password')
    street_address = StringField("Street Address", [validators.DataRequired(message="Street address is required"),
                                            validators.Length(min=2, max=100)])
    city = StringField("City", [validators.DataRequired(message="City is required"),
                                            validators.Length(min=2, max=100)])
    state = StringField("State", [validators.DataRequired(message="State is required"),
                                            validators.Length(min=2, max=100)])
    zip_code = StringField("Zip Code", [validators.DataRequired(message="Zip code is required"),
                                            validators.Length(min=4, max=100)])
    country = StringField("Country", [validators.DataRequired(message="Country is required"),
                                            validators.Length(min=3, max=100)])



# route to sign up new user
@auth_routes.route("/auth/signup", methods=["GET","POST"])
@limiter.limit("10/minute") 
def signup():
    """Function to get data for signup from new user"""

    form = SignupForm()
    if current_user.is_authenticated:
        return redirect(url_for("machine_routes.machines"))
    
    # Check if the form is submitted and valid
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        email_address = form.email_address.data
        password = form.password.data
        street_address = form.street_address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        country = form.country.data

        # Check if the user is already registered
        user = User.query.filter_by(email_address=email_address).first()

        if user is not None:
            flash("Email address already exists. Please login!", category="error")
        else:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email_address=email_address,
                password=generate_password_hash(password, method="sha256"),
                street_address=street_address,
                city=city,
                state=state,
                zip_code=zip_code,
                country=country
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash(f"Thanks for signing up, {first_name}!", category="success")
            return redirect(url_for("auth_routes.login"))

    return render_template("signup.html", form=form, user=current_user)

                

# creating form class meta data for login user
class LoginForm(FlaskForm):
    """ form class for login data"""
    email_address = EmailField("Email Address", [validators.DataRequired(message="Email address is required"),
                                            validators.Length(min=6, max=100)])
    password = PasswordField('New Password', [validators.DataRequired(message="Password is required"),
                                              validators.Length(min=8, max=100)])
    

#routes for login existing user
@auth_routes.route("/auth/login", methods=["GET", "POST"])
@limiter.limit("10/minute") 
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("machine_routes.machines"))
    
    if form.validate_on_submit():
        email_address = form.email_address.data
        password = form.password.data

        user = User.query.filter_by(email_address=email_address).first()
        if user is None:
            flash("Email address is not associated with any account. please signup!", category="error")
        else:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for("machine_routes.machines"))
            else:
                flash("Password is incorrect. Try again!", category="error")

    return render_template("login.html", form=form, user=current_user)


# creating form class for forget password
class ForgetPassword(FlaskForm):
    email_address = StringField('Email Address',[validators.DataRequired(message="Email is required"),validators.Length(min=8, max=100)])


# route for forget password
@auth_routes.route('/auth/forget_password', methods=['GET', 'POST'])
@limiter.limit("10/minute") 
def forget_password():

    form = ForgetPassword()
    if form.validate_on_submit():
        email_address = form.email_address.data
        user = User.query.filter_by(email_address=email_address).first()
        if user is not None:
            # Generate a reset token
            reset_token = secrets.token_hex(16)  
            # Store the reset token in the database or cache
            user.reset_token = reset_token
            db.session.commit()

            # Compose the email message
            msg = Message('Password Reset Request', sender='abiolaadedayo1993@gmail.com', recipients=[email_address])
            reset_url = url_for('auth_routes.reset_password', token=reset_token, _external=True)
            msg.body = f"Please click the following link to reset your password: {reset_url}"

            # Send the email
            mail.send(msg)

            flash("Check your email to continue!", category="success")
            return redirect(url_for("auth_routes.login"))
        else:
            flash("Email address is not associated with any account. Please sign up!", category="error")
            return redirect(url_for("auth_routes.signup"))
    return render_template("forget_password.html", form=form)



# creating form class for password reset
class ResetPassword(FlaskForm):
    password = PasswordField('New Password', [validators.DataRequired(message="Password is required"),
                                              validators.EqualTo('confirm', message='Passwords must match'),
                                              validators.Length(min=8, max=100)])
    confirm = PasswordField('Repeat Password')


# route for reset password
@auth_routes.route('/auth/reset_password/<token>', methods=['GET', 'POST'])
@limiter.limit("10/minute") 
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user:
        flash("Invalid or expired reset token. Please try again.", category="error")
        return redirect(url_for("auth_routes.forget_password"))

    form = ResetPassword()
    if form.validate_on_submit():
        # Update the user's password
        user.password = generate_password_hash(form.password.data, method="sha256")
        user.reset_token = None
        db.session.commit()

        flash("Your password has been reset successfully. You can now log in with your new password.", category="success")
        return redirect(url_for("auth_routes.login"))

    return render_template("reset_password.html", form=form, token=token)


@auth_routes.route("/auth/logout")
@limiter.limit("10/minute") 
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))