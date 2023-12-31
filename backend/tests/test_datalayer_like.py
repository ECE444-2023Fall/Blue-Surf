import sys
import logging

from .test_datalayer import test_client

from ..app import app
from ..datalayer.like import LikeDataLayer
from ..datalayer.tag import TagDataLayer
from ..datalayer.event import EventDataLayer
from ..datalayer.user import UserDataLayer
from ..models import User, Event, Like


def test_user_liked_event(test_client):
    user = UserDataLayer()
    event = EventDataLayer()
    tag = TagDataLayer()

    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )

        retrievedUser = user.get_user(user_identifier="testuser1")

        tag.add_tag("Tag 1")
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"],
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists is not None
        user_exists = User.query.filter_by(username="testuser1").first()
        assert user_exists is not None

    user_liked_event = LikeDataLayer()
    try:
        user_liked_event.like_by_id(user_id=user_exists.id, event_id=event_exists.id)
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert (
            Like.query.filter_by(
                user_id=user_exists.id, event_id=event_exists.id
            ).first()
            != None
        )
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists.like_count == 1


def test_event_not_exist(test_client):
    user = UserDataLayer()

    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )

    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists is None
        user_exists = User.query.filter_by(username="testuser1").first()
        assert user_exists is not None

    user_liked_event = LikeDataLayer()
    try:
        user_liked_event.like_by_id(user_id=user_exists.id, event_id=2)
    except ValueError as value_error:
        logging.debug(f"Event does not exist")
        assert str(value_error) == "Event does not exist"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert Like.query.filter_by(user_id=user_exists.id, event_id=2).first() == None


def test_user_not_exist(test_client):
    event = EventDataLayer()
    tag = TagDataLayer()
    user = UserDataLayer()

    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )

        retrievedUser = user.get_user(user_identifier="testuser1")

        tag.add_tag("Tag 1")
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"],
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists is not None
        user_exists = User.query.filter_by(id=retrievedUser.id + 1).first()
        assert user_exists is None

    user_liked_event = LikeDataLayer()
    try:
        user_liked_event.like_by_id(user_id=2, event_id=event_exists.id)
    except ValueError as value_error:
        logging.debug(f"User does not exist")
        assert str(value_error) == "User does not exist"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert Like.query.filter_by(user_id=2, event_id=event_exists.id).first() == None


def test_user_liked_event_delete(test_client):
    user = UserDataLayer()
    event = EventDataLayer()
    tag = TagDataLayer()

    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        retrievedUser = user.get_user(user_identifier="testuser1")
        tag.add_tag("Tag 1")
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"],
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists is not None
        user_exists = User.query.filter_by(username="testuser1").first()
        assert user_exists is not None

    user_liked_event = LikeDataLayer()
    try:
        user_liked_event.like_by_id(user_id=user_exists.id, event_id=event_exists.id)
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert (
            Like.query.filter_by(
                user_id=user_exists.id, event_id=event_exists.id
            ).first()
            != None
        )
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists.like_count == 1

    try:
        user_liked_event.unlike_by_id(user_id=user_exists.id, event_id=event_exists.id)
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert (
            Like.query.filter_by(
                user_id=user_exists.id, event_id=event_exists.id
            ).first()
            == None
        )
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists.like_count == 0

    # Test deleting something that already does not exist - Should not cause an error.
    try:
        user_liked_event.unlike_by_id(user_id=user_exists.id, event_id=event_exists.id)
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert (
            Like.query.filter_by(
                user_id=user_exists.id, event_id=event_exists.id
            ).first()
            == None
        )
        event_exists = Event.query.filter_by(title="Event 1").first()
        assert event_exists.like_count == 0


def test_user_liked_events(test_client):
    user = UserDataLayer()
    event = EventDataLayer()
    tag = TagDataLayer()

    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )

        retrievedUser = user.get_user(user_identifier="testuser1")

        user.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )

        retrievedUser2 = user.get_user(user_identifier="testuser2")
        tag.add_tag("Tag 1")
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser2.id,
            club="Club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"],
        )
        event.create_event(
            title="Event 2",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"],
        )
        event.create_event(
            title="Event 3",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"],
        )
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    with app.app_context():
        event1 = Event.query.filter_by(title="Event 1").first()
        event2 = Event.query.filter_by(title="Event 2").first()
        event3 = Event.query.filter_by(title="Event 3").first()
        assert event1 is not None
        user1 = User.query.filter_by(username="testuser1").first()
        assert user1 is not None

    user_liked_event = LikeDataLayer()
    try:
        # testuser1 likes event1
        user_liked_event.like_by_id(user_id=user1.id, event_id=event1.id)
        # get the events that testuser1 likes
        liked_events = user_liked_event.get_liked_events(user_id=user1.id)

    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(liked_events) == 1
    assert liked_events[0].title == "Event 1"

    try:
        user_liked_event.like_by_id(user_id=user1.id, event_id=event2.id)
        liked_events = user_liked_event.get_liked_events(user_id=user1.id)
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(liked_events) == 2
    assert liked_events[0].title == "Event 1"
    assert liked_events[1].title == "Event 2"
