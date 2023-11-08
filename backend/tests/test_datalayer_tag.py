import logging

from .test_datalayer import test_client

from ..app import app
from ..datalayer.tag import TagDataLayer
from ..datalayer.event import EventDataLayer
from ..datalayer.user import UserDataLayer
from ..models import Tag

def test_add_tag(test_client):
    tag = TagDataLayer()
    tag_name = "Test Tag"
    try: 
        tag.add_tag(tag_name=tag_name)
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        logging.warning(Tag.query.filter_by(name=tag_name))
        assert Tag.query.filter_by(name=tag_name).first() != None
    
def test_get_all_tags(test_client):
    tag = TagDataLayer()
    try: 
        tag.add_tag(tag_name="Tag 1")
        tag.add_tag(tag_name="Tag 2")
        tag.add_tag(tag_name="Tag 3")
        tags = tag.get_all_tags()
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        logging.warning(f"All tags: {tags}")
        assert "Tag 1" in tags
        assert "Tag 2" in tags
        assert "Tag 3" in tags

def test_get_tag_names_by_id(test_client):
    tag = TagDataLayer()
    try: 
        tag.add_tag(tag_name="Tag 1")
        tag.add_tag(tag_name="Tag 2")
        tag.add_tag(tag_name="Tag 3")
        tags = tag.get_tag_names_by_ids([1,2,3])
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        logging.warning(f"All tags: {tags}")
        assert "Tag 1" in tags
        assert "Tag 2" in tags
        assert "Tag 3" in tags

def test_get_events_by_tag_names(test_client):
    tag = TagDataLayer()
    event = EventDataLayer()
    user = UserDataLayer()
    try: 
        tag.add_tag(tag_name="Tag 1")
        tag.add_tag(tag_name="Tag 2")
        tag.add_tag(tag_name="Tag 3")

        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword"
        )

        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            club="club 1",
            is_published=True,
            image=None,
            tags=["Tag 1", "Tag 2"]
        )
        event.create_event(
            title="Event 2",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            club="club 1",
            is_published=True,
            image=None,
            tags=["Tag 1"]
        )
        event.create_event(
            title="Event 3",
            description="Kickoff event 1 for club 1",
            extended_description="Extended decription for event 1 for club 1 that is much longer than just the description",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            club="club 1",
            is_published=True,
            image=None,
        )
        event_ids = tag.get_events_by_tag_names(["Tag 1"])
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        logging.warning(f"All events: {event_ids}")
        assert 1 in event_ids
        assert 2 in event_ids
        assert 3 not in event_ids
    
    try:
        event_ids = tag.get_events_by_tag_names(["Tag 1", "Tag 2"])
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        logging.warning(f"All events: {event_ids}")
        assert 1 in event_ids
        assert 2 in event_ids
        assert 3 not in event_ids
    
    try:
        event_ids = tag.get_events_by_tag_names([])
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None
    
    with app.app_context():
        logging.warning(f"All events: {event_ids}")
        assert len(event_ids) == 0