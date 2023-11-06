import sys
import pytest
import logging

from .test_datalayer import test_client

sys.path.append("../")
from app import app
from datalayer_tag import TagDataLayer
from models import Tag

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
