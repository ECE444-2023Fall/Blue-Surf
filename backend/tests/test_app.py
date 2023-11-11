from ..app import app
from .test_datalayer import test_client
from ..datalayer.event import EventDataLayer
from ..datalayer.user import UserDataLayer
from ..datalayer.tag import TagDataLayer
import logging
from datetime import datetime


def setup(test_client):
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

        tag.add_tag("Tag 1")

        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name="testuser1",
            club="Club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"],
        )
    except (ValueError, TypeError) as e:
        logging.debug(f"Error: {e}")
        assert e is None


def tear_down(test_client):
    user = UserDataLayer()
    event = EventDataLayer()
    tag = TagDataLayer()

    try:
        user.delete_user_by_username("testuser1")
        event.delete_event_by_id(1)
        tag.delete_tag("Tag 1")
    except (ValueError, TypeError) as e:
        logging.debug(f"Error: {e}")
        assert e is None


def test_api_landing_page(test_client):
    setup(test_client)
    try:
        response = test_client.get("/api/")
    except (ValueError, TypeError) as e:
        assert e is None
    assert response.status_code == 200
    tear_down(test_client)


def test_api_event_details(test_client):
    setup(test_client)
    try:
        response = test_client.get("/api/1")
    except (ValueError, TypeError) as e:
        assert e is None
    assert response.status_code == 200
    assert response.json["title"] == "Event 1"
    tear_down(test_client)


def test_api_update_event(test_client):
    setup(test_client)
    try:
        response = test_client.post(
            "/api/update-post/1",
            json={
                "title": "Updated Event 1",
                "description": "Updated description",
                "extended_description": "Updated extended description",
                "location": "Updated location",
                "start_time": "2023-10-03 03:30:00",
                "end_time": "2023-10-03 04:00:00",
                "is_published": True,
                "tags": ["Tag 1"],
            },
        )
    except (ValueError, TypeError) as e:
        assert e is None
    assert response.status_code == 200
    assert response.json["message"] == "Post updated successfully"
    event = EventDataLayer()
    updated_event = event.get_event_by_id(1)
    assert updated_event.title == "Updated Event 1"
    assert updated_event.description == "Updated description"
    assert updated_event.extended_description == "Updated extended description"
    assert updated_event.location == "Updated location"
    assert updated_event.start_time == datetime.strptime(
        "2023-10-03 03:30:00", "%Y-%m-%d %H:%M:%S"
    )
    assert updated_event.end_time == datetime.strptime(
        "2023-10-03 04:00:00", "%Y-%m-%d %H:%M:%S"
    )
    assert updated_event.is_published is True
    tear_down(test_client)


def test_update_event(test_client):
    setup(test_client)
    try:
        response = test_client.post(
            "/api/update-post/1",
            json={
                "title": "Updated Event 1",
                "description": "Updated description",
                "extended_description": "Updated extended description",
            },
        )
    except (ValueError, TypeError) as e:
        assert e is None
    assert response.status_code == 500
    assert response.json["error"] == "Failed to update post"
    event = EventDataLayer()
    updated_event = event.get_event_by_id(1)
    assert updated_event.title == "Event 1"
    tear_down(test_client)
