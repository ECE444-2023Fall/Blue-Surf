import logging

from .test_datalayer import test_client

from ..app import app, db
from ..datalayer_user import UserDataLayer
from ..models import User

def test_user_creation(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
     
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None

def test_add_duplicate_username(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert str(value_error) == "Username testuser1 already exists"
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None

def test_add_duplicate_email(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        user.create_user(
            username="testuser2",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert str(value_error) == "Email testuser1@example.com already exists"
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert User.query.filter_by(username="testuser2").first() == None

def test_null_username(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username=None,
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Username should not be empty"
    
    with app.app_context():
        assert User.query.filter_by(username=None).first() == None

def test_null_email(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email=None,
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Email should not be empty"
    
    with app.app_context():
        assert User.query.filter_by(email=None).first() == None

def test_empty_username(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Username should not be empty"
    
    with app.app_context():
        assert User.query.filter_by(username="").first() == None

def test_empty_email(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Email should not be empty"
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None

def test_null_password_hash(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash=None,
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Password_hash should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None

def test_empty_password_hash(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Password_hash should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None

def test_null_password_salt(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Password_salt should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None

def test_empty_password_salt(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Password_salt should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None
