from ..app import app, db
from ..models import Tag, Event
from .abstract import DataLayer
import logging

"""
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
"""


class TagDataLayer(DataLayer):
    """
    The TagDataLayer should be accessed by the rest of the code when trying to access the Tag table in the database.
    """

    def get_all_tags(self):
        """
        Returns a list of strings containing all the existing tags in the database.
        """
        with app.app_context():
            tags = Tag.query.all()
        tag_names = [tag.name for tag in tags]
        return tag_names

    def add_tag(self, tag_name: str):
        """
        Inserts the given tag name into the Tag table in the database.
        """
        # Check if a tag with the same name already exists
        with app.app_context():
            existing_tag = Tag.query.filter_by(name=tag_name).first()

        if existing_tag is None:  # No existing tag with the same name
            tag = Tag()
            tag.name = tag_name
            with app.app_context():
                db.session.add(tag)
                db.session.commit()
        else:
            logging.warning(f"Tag {tag_name} {self.ALREADY_EXISTS}")

    def delete_tag(self, tag_name: str):
        """
        Removes the given tag name from the Tag table in the database.
        """
        # Check if a tag with the same name already exists
        with app.app_context():
            existing_tag = Tag.query.filter_by(name=tag_name).first()

            if existing_tag is None:  # No existing tag with the same name
                logging.warning(f"Tag {tag_name} {self.DOES_NOT_EXIST}")
            else:
                db.session.delete(existing_tag)
                db.session.commit()

    def get_tag_names_by_ids(self, tag_ids):
        """
        Fetch the tag names for the collected tag IDs
        """
        with app.app_context():
            names = []
            for id in tag_ids:
                assert type(id) == int
                tag = Tag.query.filter_by(id=id).first()
                if tag is not None:
                    names.append(tag.name)
            return names

    def get_events_by_tag_names(self, tag_names):
        """
        Returns a list of event_ids that contain at least one of the given tags.
        """
        with app.app_context():
            matching_tags = Tag.query.filter(Tag.name.in_(tag_names)).all()
            if not matching_tags:
                return []

            matching_events = Event.query.filter(
                Event.tags.any(Tag.id.in_([tag.id for tag in matching_tags]))
            ).all()
            event_ids = [event.id for event in matching_events]
            return event_ids
