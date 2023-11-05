import os
import sys
import pytest
from datetime import datetime
import json
import logging

sys.path.append("../")
from app import app, db
from models import User, Event, UserInterestedEvent

@pytest.fixture(scope="function")
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
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

def test_registration(test_client):
    """ Test for user registration """
    with test_client:
        response = test_client.post(
            '/auth/register',
            data=json.dumps(dict(
                email='joe@gmail.com',
                password='123456'
            )),
            content_type='application/json'
        )
        logging.debug(response.data.decode())
        data = json.loads(response.data.decode())
        assert data['status'] == 'success'
        assert data['message'] == 'Successfully registered.'
        assert data['auth_token'] == True
        assert response.content_type == 'application/json'
        assert response.status_code == 201