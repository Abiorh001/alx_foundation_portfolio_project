import pytest
from malzahratech import create_app

@pytest.fixture(scope='module')
def test_client():

    flask_app = create_app()

    # Set the Testing configuration prior to creating the Flask application
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://testdb.db'

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
