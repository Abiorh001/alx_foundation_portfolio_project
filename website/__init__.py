""" the main flask script to run the whole application """

from flask import Flask, url_for, redirect
from website.models import db, User, Machine
from website.config import Config, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address








#creating rate limit
limiter = Limiter(key_func=get_remote_address)


# initializing mail for email sender
mail = Mail()

# initializing migrate for database table schema
migrate = Migrate()



def create_app():
    """ the function that start the flask application """

    app = Flask(__name__, template_folder="/home/abiorh/malzahratech/website/app/templates",
                 static_folder="/home/abiorh/malzahratech/website/app/static")

    # Load the configuration from the Config class
    app.config.from_object(Config)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

 


    # initializing and creating the database
    db.init_app(app)
    with app.app_context():
        migrate.init_app(app, db)
        db.create_all()

    
    #initialize rate limit
    limiter.init_app(app)
    
     # Initialize the Mail extension with app context
    mail.init_app(app)





    # rendering our auth routes Blueprint
    from website.app.auth_routes import auth_routes
    app.register_blueprint(auth_routes)

    # rendering our views routes Blueprint
    from website.app.views import views
    app.register_blueprint(views)

    # rendering our machine routes Blueprint
    from website.app.machine_routes import machine_routes
    app.register_blueprint(machine_routes)

    # rendering our machine maintenance report routes Blueprint
    from website.app.machine_maintenance_report_routes import machine_maintenance_report_routes
    app.register_blueprint(machine_maintenance_report_routes)


     # rendering our machine maintenance notification routes Blueprint
    from website.app.maintenance_notification import maintenance_notification
    app.register_blueprint(maintenance_notification)

    # # rendering our machine maintenance schedule routes Blueprint
    from website.app.maintenance_schedule import maintenance_schedule
    app.register_blueprint(maintenance_schedule)

    login_manager = LoginManager()
    login_manager.login_view = "auth_routes.login"
    login_manager.init_app(app)
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('views.home'))
    

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


    return app




