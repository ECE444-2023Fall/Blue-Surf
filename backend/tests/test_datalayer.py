import os
import sys
import pytest
from datetime import datetime
import logging

sys.path.append("../")
from app import app, db
from datalayer_user import UserDataLayer
from datalayer_event import EventDataLayer
from models import User, Event, UserInterestedEvent


@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tests/db/test_datalayer.db"
    logging.basicConfig(level=logging.DEBUG)
    with app.app_context():
        if not hasattr(app, "extensions"):
            app.extensions = {}
        if "sqlalchemy" not in app.extensions:
            db.init_app(app)
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        db.drop_all()


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
        assert User.query.filter_by(username='testuser1').first() != None

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
        assert User.query.filter_by(username='testuser1').first() != None

def test_add_duplicate_email(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username="testuser3",
            email="testuser3@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        user.create_user(
            username="testuser4",
            email="testuser3@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert str(value_error) == "Email testuser3@example.com already exists"
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert User.query.filter_by(username='testuser3').first() != None
        assert User.query.filter_by(username='testuser4').first() == None

def test_null_username(test_client):
    user = UserDataLayer()
    try: 
        user.create_user(
            username=None,
            email="testuser5@example.com",
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
            username="testuser6",
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
            email="testuser7@example.com",
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
            username="testuser6",
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
        assert User.query.filter_by(email="").first() == None