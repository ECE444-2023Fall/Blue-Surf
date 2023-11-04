import os
import sys
import pytest
from datetime import datetime

sys.path.append("../")
from app import app, db
from models import User, Event, UserInterestedEvent


@pytest.fixture(scope="module")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tests/db/test_database.db"
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
    user = User(
        username="testuser",
        email="testuser@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(username="testuser").first()
        assert retrieved_user.username == "testuser"
        assert retrieved_user.email == "testuser@example.com"


def test_event_creation(test_client):
    start_time = datetime.strptime("2023-10-28 09:00:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2023-10-28 11:00:00", "%Y-%m-%d %H:%M:%S")

    # Read the image file
    image_file_path = os.path.join("../../images", "logo.png")
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()

    event = Event(
        title="Test Event",
        description="Test Event Description",
        location="online",
        start_time=start_time,
        end_time=end_time,
        author=None,
        is_published=True,
        like_count=0,
        image=image_data,
    )

    with app.app_context():
        db.session.add(event)
        db.session.commit()

        retrieved_event = Event.query.filter_by(title="Test Event").first()
        assert retrieved_event.title == "Test Event"
        assert retrieved_event.is_published == True
        assert retrieved_event.image is not None
        assert retrieved_event.image == image_data


def test_user_update_password(test_client):
    """
    This is a unit test added by Meriam Fourati (for Lab 5).
    This tests verifies that a value can be updated once an entry
    is added in the database.
    """
    user = User(
        username="testuser2",
        email="testuser2@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()

    # Update the user's password
    new_password = "newpassword"
    with app.app_context():
        user = User.query.filter_by(username="testuser2").first()
        user.password_hash = new_password
        db.session.commit()

    # Verify that the user's password has been updated
    with app.app_context():
        updated_user = User.query.filter_by(username="testuser2").first()
        assert updated_user.password_hash == new_password
        
def test_user_interested_event_relationship(test_client):
    """
    This is a unit test added by Jioh Kim (For Lab 5).
    This test checks if a user can express interest in an event and if that relationship
    is stored correctly in the UserInterestedEvent table.
    """
    user = User(
        username="testuser3",
        email="testuser3@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    start_time = datetime.strptime("2023-11-03 04:20:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2023-11-03 12:00:00", "%Y-%m-%d %H:%M:%S")
    event = Event(
        title="Test Event 2",
        description="Test Event Description 2",
        location="online",
        start_time=start_time,
        end_time=end_time,
        author=None,
        is_published=True,
        like_count=0,
    )

    with app.app_context():
        db.session.add(user)
        db.session.add(event)
        db.session.commit()

        # Create a relationship between the user and the event
        user_from_db = User.query.filter_by(username="testuser3").first()
        event_from_db = Event.query.filter_by(title="Test Event 2").first()
        
        user_event_relationship = UserInterestedEvent(
        user_id=user_from_db.id,
        event_id=event_from_db.id
        )
        db.session.add(user_event_relationship)
        db.session.commit()

        # Verify the relationship was created
        relationship = UserInterestedEvent.query.filter_by(
            user_id=user_from_db.id, event_id=event_from_db.id
        ).first()
        
        assert relationship is not None
        
        #!!! Additionally, we can use the relationships defined in our models to verify !!!
        assert user_from_db in event_from_db.interested_users
        assert event_from_db in user_from_db.events_interested

