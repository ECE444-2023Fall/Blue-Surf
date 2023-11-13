from datetime import datetime
import logging
from PIL import Image
import io
import os
from pathlib import Path

from .test_datalayer import test_client

from ..app import app
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
            start_time="2023-10-05 6:00:00",
            end_time="2023-10-06 4:00:00",
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
        assert new_event.description == "Kickoff event CHANGED for club 1"
        assert (
            new_event.extended_description
            == "Extended decription for event 1 CHANGED for club 1 that is much longer than just the description"
        )
        assert new_event.location == "Toronto"
        assert new_event.start_time == datetime.strptime(
            "2023-10-05 6:00:00", "%Y-%m-%d %H:%M:%S"
        )
        assert new_event.end_time == datetime.strptime(
            "2023-10-06 4:00:00", "%Y-%m-%d %H:%M:%S"
        )
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
    user1_id = user.create_user(
        username="testuser10",
        email="testuser10@example.com",
        password_hash="testpassword",
        password_salt="testpassword",
    )

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
        author_id=user1_id,
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
            start_time="2023-10-05 6:00:00",
            end_time="2023-10-06 4:00:00",
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
        user1_id = user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
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

        event.create_event(
            title="Event 2",
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
        with app.app_context():
            user_id = User.query.filter_by(username="testuser1").first().id

        events_authored = event.get_authored_events(author_id=user_id)

    except (ValueError, TypeError) as error:
        logging.debug(f"Error: {error}")
        assert error == None

    assert len(events_authored) == 2
    assert events_authored[0].title == "Event 1"
    assert events_authored[1].title == "Event 2"
