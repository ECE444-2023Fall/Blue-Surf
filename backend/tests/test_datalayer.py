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
    with app.app_context():
        if not hasattr(app, "extensions"):
            app.extensions = {}
        if "sqlalchemy" not in app.extensions:
            db.init_app(app)
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        # db.drop_all()


# def test_user_creation(test_client):
#     user = UserDataLayer()

#     try: 
#         user.create_user(
#             username="testuser1",
#             email="testuser1@example.com",
#             password_hash="testpassword",
#             password_salt="testpassword",
#         )
#     except ValueError as value_error: 
#         logging(f'Error: {value_error}')
#     except TypeError as type_error:
#         logging(f'Error: {type_error}')

    

    # assert User.query.filter_by(username='testuser1').first() != None
