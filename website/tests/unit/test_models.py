import pytest
from malzahratech.models import db, User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def new_user():
    password = generate_password_hash('FlaskIsAwesome')
    user = User('abiola', 'adeshina', '08023071316', 'abiolatest@gmail.com',password,
                    'kuforiji', 'abeokuta', 'ogun', '110011', 'nigeria')
    return user

def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, phone_number,
            email_address, hashed_password, street_address, city,
            state, zip_code, and country fields are defined correctly
    """
    assert new_user.first_name == 'abiola'
    assert new_user.last_name == 'adeshina'
    assert new_user.phone_number == '08023071316'
    assert new_user.email_address == 'abiolatest@gmail.com'
    assert new_user.password != 'FlaskIsAwesome'
    assert new_user.street_address == 'kuforiji'
    assert new_user.city == 'abeokuta'
    assert new_user.state == 'ogun'
    assert new_user.zip_code == '110011'
    assert new_user.country == 'nigeria'


