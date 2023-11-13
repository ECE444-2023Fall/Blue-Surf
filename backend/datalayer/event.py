from ..app import app, db
from ..models import User, Event, Tag
from .abstract import DataLayer

from datetime import datetime
import logging
from sqlalchemy import or_
from PIL import Image
import io

"""
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    extended_description = db.Column(db.Text)
    location = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    like_count = db.Column(db.Integer, default=0)
    image = db.Column(db.LargeBinary, nullable=True)
    club = db.Column(db.Text)
    
     # Define a many-to-many relationship with tags through the event_tags table
    tags = db.relationship("Tag", secondary=event_tags)
"""


class EventDataLayer(DataLayer):
    def helper_check_times(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Given a start and end time, it returns whether both are valid.
        This means that:
        - start_time and end_time are not None
        - they are both valid datetime objects
        - start_time is before end_time
        """
        if start_time is None:
            logging.info(f"Start time {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Start time {self.SHOULD_NOT_BE_EMPTY}")
        try:
            temp_start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
            raise ValueError(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

        if end_time is None:
            logging.info(f"End time {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"End time {self.SHOULD_NOT_BE_EMPTY}")
        try:
            temp_end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
            raise ValueError(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

        if temp_end_datetime < temp_start_datetime:
            logging.info("Start time should be after end time")
            raise ValueError("Start time should be after end time")

        return True

    def helper_valid_title(self, title: str) -> bool:
        """
        Given a title, it returns whether it is valid.
        This means that:
        - title is not None
        - title is not empty
        """
        if title is None or len(title) == 0:
            logging.info(f"Title {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Title {self.SHOULD_NOT_BE_EMPTY}")
        return True

    def helper_valid_location(self, location: str) -> bool:
        """
        Given a location, it returns whether it is valid.
        This means that:
        - location is not None
        - location is not empty
        """
        if location is None or len(location) == 0:
            logging.info(f"Location {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Location {self.SHOULD_NOT_BE_EMPTY}")
        return True

    def helper_valid_author(self, author_id: int) -> bool:
        """
        Given an author_id, it returns whether it is valid.
        This means that:
        - the author exists in the database
        """
        with app.app_context():
            author = User.query.filter_by(id=author_id).first()
            if author is None:
                logging.info(f"User {author_id} {self.UNABLE_TO_POST}")
                raise TypeError(f"User {author_id} {self.UNABLE_TO_POST}")
        return True

    def helper_valid_published(self, is_published: bool) -> bool:
        """
        Given an is_published, it returns whether it is valid.
        This means that:
        - is_published is not None
        """
        if is_published is None and type(is_published) != bool:
            logging.info(f"Event {self.WAS_NOT_PUBLISHED}")
            raise TypeError(f"Event {self.WAS_NOT_PUBLISHED}")
        return True

    def helper_valid_image(self, image: bytes) -> bool:
        """
        Given an image, it returns whether it is valid.
        This means that:
        - image is not None
        - image is in the correct format
        """
        if image is not None:
            try:
                Image.open(io.BytesIO(image))
            except Exception as e:
                logging.info(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
                raise TypeError(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
        return True

    def create_event(
        self,
        title,
        description,
        extended_description,
        location,
        start_time,
        end_time,
        author_id,
        is_published,
        club,
        image=None,
        tags=None,
    ):
        """
        Creates an event with the given parameters and adds it to the database.
        Returns the id of the event.
        """
        event = Event()
        try:
            self.helper_valid_title(title)
            self.helper_valid_location(location)
            self.helper_check_times(start_time, end_time)
            self.helper_valid_author(author_id)
            self.helper_valid_published(is_published)
            self.helper_valid_image(image)

        except (ValueError, TypeError) as e:
            raise e

        event.title = title
        event.description = description
        event.extended_description = extended_description
        event.location = location
        event.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        event.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        event.author_id = author_id
        event.is_published = is_published
        event.club = club
        event.image = image

        with app.app_context():
            # Add the event to the database
            db.session.add(event)
            db.session.commit()

            event.tags = []
            if tags:
                for tag_name in tags:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if tag is not None:
                        event.tags.append(tag)

            # Commit the changes to the session after adding tags
            db.session.commit()
            return event.id

    def get_search_results_by_keyword(self, keyword):
        keyword_word_pattern = "% {}%".format(keyword)
        keyword_start_pattern = "{}%".format(keyword)
        with app.app_context():
            query = Event.query.filter(
                or_(
                    Event.title.ilike(keyword_word_pattern),
                    Event.club.ilike(keyword_word_pattern),
                    Event.title.ilike(keyword_start_pattern),
                    Event.club.ilike(keyword_start_pattern),
                )
            )
            results = query.all()
            return results

    def update_event(
        self,
        event_id,
        title,
        description,
        extended_description,
        location,
        image=None,
        is_published=True,
        start_time=None,
        end_time=None,
        club=None,
        tags=[],
    ):
        # get the event by event_id
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if event is None:
                logging.info(f"Event with id {event_id} {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event with id {event_id} {self.DOES_NOT_EXIST}")
            try:
                self.helper_valid_title(title)
                self.helper_valid_location(location)
                self.helper_check_times(start_time, end_time)
                self.helper_valid_published(is_published)
                self.helper_valid_image(image)

            except (ValueError, TypeError) as e:
                raise e

            event.title = title
            event.description = description
            event.extended_description = extended_description
            event.location = location
            event.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            event.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            event.is_published = is_published
            event.club = club
            event.image = image
            db.session.commit()

            event.tags = []
            if tags:
                for tag_name in tags:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if tag is not None:
                        event.tags.append(tag)

            # Commit the changes to the session after adding tags
            db.session.commit()

    def get_all_events(self):
        """
        Returns all events.
        """
        with app.app_context():
            events = Event.query.all()
            return events

    def get_event_by_id(self, id):
        """
        Returns the event with the given id.
        """
        with app.app_context():
            event = Event.query.filter_by(id=id).first()
            if event is None:
                logging.info(f"Event with id {id} {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event with id {id} {self.DOES_NOT_EXIST}")
            return event

    def delete_event_by_id(self, id):
        """
        Deletes the event with the given event id.
        """
        with app.app_context():
            event = Event.query.filter_by(id=id).first()
            if event is None:
                logging.info(f"Event with id {id} does not exist and cannot be deleted")
                raise ValueError(
                    f"Event with id {id} does not exist and cannot be deleted"
                )
            db.session.delete(event)
            db.session.commit()

    def get_authored_events(self, author_id):
        """
        Returns all events authored by the given author_id.
        """
        with app.app_context():
            events = Event.query.filter_by(author_id=author_id).all()
            if events is None:
                logging.info(f"Event with author_id {author_id} {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event with id {author_id} {self.DOES_NOT_EXIST}")
            return events

    def get_tags_for_event(self, event_id):
        """
        Returns a list of Tag objects that are associated with the given event id.
        """
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if event.tags == None:
                return []
            return event.tags

    def update_image(self, event_id, image):
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if image is not None:
                try:
                    # make sure the image can be opened (given in correct format)
                    Image.open(io.BytesIO(image))
                except Exception as e:
                    logging.info(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
                    raise TypeError(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

            event.image = image
            db.session.commit()
