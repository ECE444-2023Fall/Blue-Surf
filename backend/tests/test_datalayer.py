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


def test_event_creation(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            is_published=True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() != None

def test_null_location(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location=None,
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            is_published=True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Location should not be empty"
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_null_start_time(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time=None,
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            is_published = True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Start time should not be empty"
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_incorrect_start_time_format(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            is_published = True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert str(value_error) == "Start time is not given in correct format"
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_null_end_time(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 4:00:00",
            end_time=None,
            author_name='testuser1',
            is_published = True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "End time should not be empty"
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_incorrect_end_time_format(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03",
            author_name='testuser1',
            is_published = True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert str(value_error) == "End time is not given in correct format"
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_event_time(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 3:00:00",
            author_name='testuser2',
            is_published = True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert str(value_error) == "Start time should be after end time"
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_author_id(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser2',
            is_published = True,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Username testuser2 unable to post"
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_null_published(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    try: 
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 4:00:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            is_published=None,
            image=None,
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert str(type_error) == "Event was not published"
    
    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert Event.query.filter_by(title="Event 1").first() == None

def test_event_update(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser10',
            is_published=True,
            image=None,
        )
    try: 
        with app.app_context():
            event_id = Event.query.filter_by(title="Event 1").first().id
        event.update_event(
            event_id=event_id,
            title="Event 1 - CHANGED",
            description="Kickoff event CHANGED for club 1",
            location="Toronto",
        )
        
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        new_event = Event.query.filter_by(id=event_id).first()
        assert new_event is not None
        assert new_event.title=="Event 1 - CHANGED"

def test_get_all_events(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser10',
            is_published=True,
            image=None,
        )
    event.create_event(
            title="Event 2",
            description="Kickoff event 2 for club 2",
            location="Vancouver",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser10',
            is_published=True,
            image=None,
        )
    try: 

        events = event.get_all_events()
        
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert len(events) == 2
        assert events[0].title == "Event 1"
        assert events[1].title == "Event 2"

def test_event_by_id(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    event = EventDataLayer()
    event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser10',
            is_published=True,
            image=None,
        )
    try: 
        with app.app_context():
            event_id = Event.query.filter_by(title="Event 1").first().id
        event = event.get_event_by_id(event_id)
        
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        assert event.title == "Event 1"