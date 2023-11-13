import logging
from PIL import Image
import io
import os
from pathlib import Path

from .test_datalayer import test_client

from ..app import app, db
from ..datalayer.user import UserDataLayer
from ..datalayer.event import EventDataLayer
from ..datalayer.tag import TagDataLayer
from ..models import User, Event, Tag


def test_event_creation(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser1")
    tag = TagDataLayer()
    tag.add_tag("Tag 1")

    event = EventDataLayer()

    # Read the image file
    current_directory = os.path.dirname(__file__)
    image_directory = current_directory + "/../../images"
    image_file_path = os.path.join(image_directory, "logo.png")
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()

    try:
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
            image=image_data,
            tags=["Tag 1"],
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        user = User.query.filter_by(username="testuser1").first()
        assert user != None
        event = Event.query.filter_by(title="Event 1").first()
        assert event != None
        tag = Tag.query.filter_by(name="Tag 1").first()
        assert tag != None
        assert tag in event.tags


def test_null_location(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location=None,
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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
    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time=None,
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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
    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "Start time is not given in correct format"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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
    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 4:00:00",
            end_time=None,
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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
    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "End time is not given in correct format"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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
    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 3:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "Start time should be after end time"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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

    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id + 1,
            club="Club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == f"User {retrievedUser.id+1} unable to post"

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

    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 4:00:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="Club 1",
            is_published=None,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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
    retrievedUser = user.get_user(user_identifier="testuser10")

    tag = TagDataLayer()
    tag.add_tag("Tag 1")

    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff event 1 for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="club 1",
        is_published=True,
        image=None,
    )
    try:
        # Read the image file
        current_directory = os.path.dirname(__file__)
        image_directory = current_directory + "/../../images"
        image_file_path = os.path.join(image_directory, "logo.png")
        with open(image_file_path, "rb") as image_file:
            image_data = image_file.read()

        with app.app_context():
            event_id = Event.query.filter_by(title="Event 1").first().id
        event.update_event(
            event_id=event_id,
            title="Event 1 - CHANGED",
            description="Kickoff event CHANGED for club 1",
            extended_description="Extended decription for event 1 CHANGED for club 1 that is much longer than just the description",
            location="Toronto",
            tags=["Tag 1"],
            image=image_data,
        )

    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        new_event = Event.query.filter_by(id=event_id).first()
        assert new_event is not None
        assert new_event.title == "Event 1 - CHANGED"
        assert len(new_event.tags) == 1
        assert new_event.tags[0].name == "Tag 1"

        image_data = new_event.image
        image = Image.open(io.BytesIO(image_data))

        subdirectory_name = "output_images"

        # Create the subdirectory if it doesn't exist
        output_directory = Path.cwd() / subdirectory_name
        output_directory.mkdir(parents=True, exist_ok=True)
        output_image_path = output_directory / "retrieved_image.png"
        # Save the image to a file
        # image.save(output_image_path)


def test_event_update_delete_tag(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser10")
    tag = TagDataLayer()
    tag.add_tag("Tag 1")

    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff event 1 for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="club 1",
        is_published=True,
        image=None,
        tags=["Tag 1"],
    )
    try:
        with app.app_context():
            event_id = Event.query.filter_by(title="Event 1").first().id
        event.update_event(
            event_id=event_id,
            title="Event 1 - CHANGED",
            description="Kickoff event CHANGED for club 1",
            extended_description="Extended decription for event 1 CHANGED for club 1 that is much longer than just the description",
            location="Toronto",
            tags=[],
        )

    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        new_event = Event.query.filter_by(id=event_id).first()
        assert new_event is not None
        assert new_event.title == "Event 1 - CHANGED"
        assert len(new_event.tags) == 0


def test_get_all_events(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser10")

    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff event 1 for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="club 1",
        is_published=True,
        image=None,
    )
    event.create_event(
        title="Event 2",
        description="Kickoff event 2 for club 2",
        extended_description="Extended decription for event 2 for club 2 that is much longer than just the description",
        location="Vancouver",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="club 2",
        is_published=True,
        image=None,
    )
    try:
        events = event.get_all_events()

    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
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
    retrievedUser = user.get_user(user_identifier="testuser10")

    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff event 1 for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="club 1",
        is_published=True,
        image=None,
    )
    try:
        with app.app_context():
            event_id = Event.query.filter_by(title="Event 1").first().id
        event = event.get_event_by_id(event_id)

    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert event.title == "Event 1"


def test_null_club(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser1")

    tag = TagDataLayer()
    tag.add_tag("Tag 1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club=None,
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
        event = Event.query.filter_by(title="Event 1").first()
        assert event.club == None


def test_delete_event_by_id(test_client):
    user = UserDataLayer()
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

    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff event 1 for club 1",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        is_published=True,
        image=None,
        extended_description="An extended description",
        club="Test Club",
    )
    event.create_event(
        title="Event 2",
        description="Kickoff event 2 for club 2",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser2.id,
        is_published=True,
        image=None,
        extended_description="An extended description",
        club="Test Club",
    )
    try:
        with app.app_context():
            created_event = Event.query.filter_by(title="Event 1").first()
            assert created_event is not None
            assert created_event.title == "Event 1"
            assert created_event.author_id == retrievedUser.id
        event.delete_event_by_id(created_event.id)
        print("Deleted event")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        deleted_event = Event.query.filter_by(title="Event 1").first()
        assert deleted_event is None


def test_get_tag_ids_for_event(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    retrievedUser = user.get_user(user_identifier="testuser1")

    tag = TagDataLayer()
    tag.add_tag("Tag 1")

    event = EventDataLayer()
    try:
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            club=None,
            is_published=True,
            image=None,
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            tags=["Tag 1"],
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        event_inserted = Event.query.filter_by(title="Event 1").first()
        assert event_inserted != None

    try:
        tags = event.get_tags_for_event(event_inserted.id)
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert len(tags) == 1
        assert tags[0].name == "Tag 1"


def test_search_by_keyword(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    retrievedUser = user.get_user(user_identifier="testuser1")

    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="club 1",
        is_published=True,
        image=None,
    )
    event.create_event(
        title="Faculty party planning",
        description="Join us at our meeting",
        extended_description="Extended decription for faculty party planning, longer than the description",
        location="UC college",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Faculty Event Planning",
        is_published=True,
        image=None,
    )

    try:
        query_results = event.get_search_results_by_keyword(keyword="Ev")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert len(query_results) == 2
        assert query_results[0].title == "Event 1"
        assert query_results[1].club == "Faculty Event Planning"


def test_get_events_by_tag(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser1")
    tag = TagDataLayer()
    tag.add_tag("Tag 1")
    event = EventDataLayer()
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
    event.create_event(
        title="Event 2",
        description="Kickoff event 2 for club 1",
        extended_description="Extended decription for event 2 for club 1 that is much longer than just the description",
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
        description="Kickoff event 3 for club 1",
        extended_description="Extended decription for event 3 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Club 1",
        is_published=True,
        image=None,
        tags=["Tag 2"],
    )

    try:
        events = event.get_events_by_tag(tag_name="Tag 1")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert len(events) == 2
        assert events[0].title == "Event 1"
        assert events[1].title == "Event 2"

    try:
        events = event.get_events_by_tag(tag_name="Tag 2")
    except ValueError as value_error:
        logging.info(f"Tag does not exist")
        assert str(value_error) == "Tag does not exist"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None


def test_get_events_by_tag(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser1")
    tag = TagDataLayer()
    tag.add_tag("Tag 1")
    event = EventDataLayer()
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
    event.create_event(
        title="Event 2",
        description="Kickoff event 2 for club 1",
        extended_description="Extended decription for event 2 for club 1 that is much longer than just the description",
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
        description="Kickoff event 3 for club 1",
        extended_description="Extended decription for event 3 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Club 1",
        is_published=True,
        image=None,
        tags=["Tag 2"],
    )

    try:
        events = event.get_events_by_tag(tag_name="Tag 1")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert len(events) == 2
        assert events[0].title == "Event 1"
        assert events[1].title == "Event 2"

    try:
        events = event.get_events_by_tag(tag_name="Tag 2")
    except ValueError as value_error:
        logging.info(f"Tag does not exist")
        assert str(value_error) == "Tag does not exist"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None


def test_update_image(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    retrievedUser = user.get_user(user_identifier="testuser1")
    tag = TagDataLayer()
    tag.add_tag("Tag 1")

    event = EventDataLayer()

    # Read the image file
    current_directory = os.path.dirname(__file__)
    image_directory = current_directory + "/../../images"
    image_file_path = os.path.join(image_directory, "logo.png")
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()

    try:
        event.create_event(
            title="Event 1",
            description="Kickoff for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        event_created = Event.query.filter_by(title="Event 1").first()
        assert event != None

    try:
        event.update_image(event_id=event_created.id, image=image_data)
    except ValueError as value_error:
        assert value_error == None

    with app.app_context():
        event = Event.query.filter_by(title="Event 1").first()
        assert event is not None
        assert event.image is not None

        image_data = event.image
        image = Image.open(io.BytesIO(image_data))

        subdirectory_name = "output_images"
        # Create the subdirectory if it doesn't exist
        output_directory = Path.cwd() / subdirectory_name
        output_directory.mkdir(parents=True, exist_ok=True)

        output_image_path = output_directory / "update_image.png"
        # Save the image to a file
        # image.save(output_image_path)


def test_update_image(test_client):
    user = UserDataLayer()
    user1_id = user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

    tag = TagDataLayer()
    tag.add_tag("Tag 1")

    event = EventDataLayer()

    # Read the image file
    current_directory = os.path.dirname(__file__)
    image_directory = current_directory + "/../../images"
    image_file_path = os.path.join(image_directory, "logo.png")
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()

    try:
        event.create_event(
            title="Event 1",
            description="Kickoff for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=user1_id,
            club="club 1",
            is_published=True,
            image=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        event_created = Event.query.filter_by(title="Event 1").first()
        assert event != None

    try:
        event.update_image(event_id=event_created.id, image=image_data)
    except ValueError as value_error:
        assert value_error == None

    with app.app_context():
        event = Event.query.filter_by(title="Event 1").first()
        assert event is not None
        assert event.image is not None

        image_data = event.image
        image = Image.open(io.BytesIO(image_data))

        subdirectory_name = "output_images"
        # Create the subdirectory if it doesn't exist
        output_directory = Path.cwd() / subdirectory_name
        output_directory.mkdir(parents=True, exist_ok=True)

        output_image_path = output_directory / "update_image.png"
        # Save the image to a file
        # image.save(output_image_path)


def test_get_authored_events(test_client):
    user = UserDataLayer()
    event = EventDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        retrievedUser = user.get_user(user_identifier="testuser1")
        event.create_event(
            title="Event 1",
            description="Kickoff for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="club 1",
            is_published=True,
            image=None,
        )

        event.create_event(
            title="Event 2",
            description="Kickoff for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_id=retrievedUser.id,
            club="club 1",
            is_published=True,
            image=None,
        )
        with app.app_context():
            user_id = User.query.filter_by(username="testuser1").first().id

        events_authored = event.get_authored_events(author_id=user_id)

    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events_authored) == 2
    assert events_authored[0].title == "Event 1"
    assert events_authored[1].title == "Event 2"


def test_search_filter_sort(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser1")
    tag = TagDataLayer()
    tag.add_tag("Tag 1")
    event = EventDataLayer()
    event.create_event(
        title="Event 2",
        description="Kickoff event 2 for club 1",
        extended_description="Extended decription for event 2 for club 1 that is much longer than just the description",
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
        title="Event 1",
        description="Kickoff event 1 for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="toronto",
        start_time="2023-09-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Club 1",
        is_published=True,
        image=None,
        tags=["Tag 1"],
    )
    event.create_event(
        title="alumni event",
        description="Kickoff event 3 for club 1",
        extended_description="Extended decription for event 3 for club 1 that is much longer than just the description",
        location="Montreal",
        start_time="2023-11-03 3:30:00",
        end_time="2023-11-03 4:00:00",
        author_id=retrievedUser.id,
        club="Club 2",
        is_published=True,
        image=None,
        tags=["Tag 2"],
    )

    try:
        events = event.search_filter_sort(tag_name="Tag 1", keyword="Ev")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    with app.app_context():
        assert len(events) == 2
        assert events[0].title == "Event 2"
        assert events[1].title == "Event 1"

    try:
        events = event.search_filter_sort(tag_name="Tag 2", keyword="Ev")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 0

    try:
        # everything optional
        events = event.search_filter_sort()
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 3
    assert events[0].title == "Event 2"
    assert events[1].title == "Event 1"
    assert events[2].title == "alumni event"

    # testinng for alphabetical sorting
    try:
        events = event.search_filter_sort(sort_by="alphabetical")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 3
    assert events[0].title == "alumni event"
    assert events[1].title == "Event 1"
    assert events[2].title == "Event 2"

    # keyword, tag name, and alphabetical sorting
    try:
        events = event.search_filter_sort(
            keyword="Ev", tag_name="Tag 1", sort_by="alphabetical"
        )
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 2
    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"

    # keyword, and date sorting
    try:
        events = event.search_filter_sort(keyword="Ev", sort_by="start time")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 3
    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"
    assert events[2].title == "alumni event"

    # set the like counts
    with app.app_context():
        event1 = Event.query.filter_by(title="Event 1").first()
        event2 = Event.query.filter_by(title="Event 2").first()
        event3 = Event.query.filter_by(title="alumni event").first()
        event1.like_count = 1
        event2.like_count = 2
        event3.like_count = 3
        db.session.commit()

    # keyword, and like count sorting
    try:
        events = event.search_filter_sort(keyword="Ev", sort_by="trending")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 3
    assert events[0].title == "alumni event"
    assert events[1].title == "Event 2"
    assert events[2].title == "Event 1"

    # keyword, location and alphabetical sorting
    try:
        events = event.search_filter_sort(
            keyword="Ev", location="Toronto", sort_by="alphabetical"
        )
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 2
    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"

    # keyword, location and alphabetical sorting
    try:
        events = event.search_filter_sort(keyword="Ev", club="Club 1")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 2
    assert events[0].title == "Event 2"
    assert events[1].title == "Event 1"

    # filtering by complete date string
    try:
        events = event.search_filter_sort(start_time="2023-10-03 3:30:00")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 1
    assert events[0].title == "Event 2"

    # filtering by partial date string
    try:
        events = event.search_filter_sort(start_time="2023-10-03")
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 1
    assert events[0].title == "Event 2"

    # filtering by date string interval
    try:
        events = event.search_filter_sort(
            start_time="2023-11-03 3:30:00", end_time="2023-11-03 4:00:00"
        )
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 1
    assert events[0].title == "alumni event"

    # filtering by partial date string interval
    try:
        events = event.search_filter_sort(
            start_time="2023-09-03", end_time="2023-10-03", sort_by="alphabetical"
        )
    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events) == 2
    assert events[0].title == "Event 1"
    assert events[1].title == "Event 2"


def test_get_all_locations(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser10")
    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff event 1 for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Tenzino fan club",
        is_published=True,
        image=None,
    )
    event.create_event(
        title="Event 2",
        description="Kickoff event 2 for club 2",
        extended_description="Extended decription for event 2 for club 2 that is much longer than just the description",
        location="Vancouver",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Dawson fan club",
        is_published=True,
        image=None,
    )
    event.create_event(
        title="Event 3",
        description="Kickoff event 2 for club 2",
        extended_description="Extended decription for event 2 for club 2 that is much longer than just the description",
        location="Calgary",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Bluesurf fan club",
        is_published=True,
        image=None,
    )
    try:
        locations = event.get_all_locations()

    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert len(locations) == 3
        assert locations[0] == "Toronto"
        assert locations[1] == "Vancouver"
        assert locations[2] == "Calgary"


def test_get_all_clubs(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )
    retrievedUser = user.get_user(user_identifier="testuser10")
    event = EventDataLayer()
    event.create_event(
        title="Event 1",
        description="Kickoff event 1 for club 1",
        extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
        location="Toronto",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Tenzino fan club",
        is_published=True,
        image=None,
    )
    event.create_event(
        title="Event 2",
        description="Kickoff event 2 for club 2",
        extended_description="Extended decription for event 2 for club 2 that is much longer than just the description",
        location="Vancouver",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Dawson fan club",
        is_published=True,
        image=None,
    )
    event.create_event(
        title="Event 3",
        description="Kickoff event 2 for club 2",
        extended_description="Extended decription for event 2 for club 2 that is much longer than just the description",
        location="Calgary",
        start_time="2023-10-03 3:30:00",
        end_time="2023-10-03 4:00:00",
        author_id=retrievedUser.id,
        club="Bluesurf fan club",
        is_published=True,
        image=None,
    )
    try:
        clubs = event.get_all_clubs()

    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert len(clubs) == 3
        assert clubs[0] == "Tenzino fan club"
        assert clubs[1] == "Dawson fan club"
        assert clubs[2] == "Bluesurf fan club"
