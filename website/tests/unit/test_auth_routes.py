import unittest
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user
from malzahratech.models import db, User
from malzahratech.app.auth_routes import SignupForm

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "2524242fsfsfrhacscsq0q9x"
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(self.app)
        self.client = self.app.test_client()

        self.auth_routes = Blueprint('auth_routes', __name__)

        self.app.register_blueprint(self.auth_routes)

        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create the database
        db.create_all()

        # Create a new user
        user = User(
            first_name="John",
            last_name="Doe",
            email_address="johndoe@example.com",
            password="password",
            phone_number="123456789",
            street_address="123 Main St",
            city="Example City",
            state="Example State",
            zip_code="12345",
            country="Example Country"
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        form = SignupForm()
        form.first_name.data = "John"
        form.last_name.data = "Doe"
        form.email_address.data = "johndoe@example.com"
        form.password.data = "password"
        form.confirm.data = "password"

        response = self.client.post("/auth/signup", data=form.data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(current_user.is_authenticated)
        self.assertEqual(current_user.email_address, "johndoe@example.com")

    def test_login(self):
        response = self.client.post("/auth/login", data={
            "email_address": "johndoe@example.com",
            "password": "password"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(current_user.is_authenticated)
        self.assertEqual(current_user.email_address, "johndoe@example.com")

    def test_login_with_invalid_credentials(self):
        response = self.client.post("/auth/login", data={
            "email_address": "johndoe@example.com",
            "password": "invalid"
        })

        self.assertEqual(response.status_code, 401)
        self.assertFalse(current_user.is_authenticated)

    def test_logout(self):
        self.client.post("/auth/login", data={
            "email_address": "johndoe@example.com",
            "password": "password"
        })

        self.assertTrue(current_user.is_authenticated)

        response = self.client.get("/auth/logout")

        self.assertEqual(response.status_code, 302)
        self.assertFalse(current_user.is_authenticated)

if __name__ == '__main__':
    unittest.main()
