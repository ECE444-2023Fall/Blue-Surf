import logging
from datetime import datetime

from ..app import app, db
from ..models import User, Event, Tag
from .abstract import DataLayer


'''
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    like_count = db.Column(db.Integer, default=0)
    image = db.Column(db.LargeBinary, nullable=True)
    club = db.Column(db.Text)
'''

class EventDataLayer(DataLayer):
    def helper_valid_times(self,start_time: datetime, end_time: datetime) -> bool:
        '''
        Given a start and end time, it returns whether both are valid.
        This means that:
        - start_time and end_time are not None
        - they are both valid datetime objects
        - start_time is before end_time
        '''
        if start_time is None or end_time is None:
            return False
        try:
            start = datetime(start_time)
            end = datetime(end_time)
        except Exception as e:
            raise e 

        if end < start:
            return False     
        
        return True

    def create_event(self, title, description, extended_description, location, start_time, end_time, author_name, is_published, club, image=None, tags=None):
        event = Event()

        if title is None or len(title) == 0:
            logging.info(f"Title {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Title {self.SHOULD_NOT_BE_EMPTY}")
        if len(title) > 255:
            logging.info(f"Title {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
            raise ValueError(f"Title {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
        event.title = title

        #TODO: Implement some checks for description?
        event.description = description
        
        #TODO: Implement some checks for extended description?
        event.extended_description = extended_description

        if location is None or len(location) == 0:
            logging.info(f"Location {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Location {self.SHOULD_NOT_BE_EMPTY}")
        if len(location) > 255:
            logging.info(f"Location {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
            raise ValueError(f"Location {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
        event.location = location

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
        event.start_time = temp_start_datetime
        event.end_time = temp_end_datetime
        
        #TODO: Implement some checks for club?
        event.club = club

        with app.app_context():
            author = User.query.filter_by(username=author_name).first()
            if author is None:
                logging.info(f"Username {author_name} {self.UNABLE_TO_POST}")
                raise TypeError(f"Username {author_name} {self.UNABLE_TO_POST}")
            event.author_id = author.id

            if is_published is None:
                logging.info(f"Event {self.WAS_NOT_PUBLISHED}")
                raise TypeError(f"Event {self.WAS_NOT_PUBLISHED}")
            event.is_published = is_published

            # Add the event to the database
            db.session.add(event)
            db.session.commit()

            # Associate tags with the event
            logging.warning(f"Tags is {tags}")
            if tags:
                for tag_name in tags:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if tag is not None:
                        event.tags.append(tag) 

            # Commit the changes to the session after adding tags
            db.session.commit()


    def update_event(self, event_id, title, description, extended_description, location, image=None, is_published=True, start_time=None, end_time=None):
        # get the event by event_id
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if event is None:
                logging.info(f"Event with id {event_id} does not exist")
                raise ValueError(f"Event with id {event_id} does not exist")
                
            # UPDATE event in db
            if title is None or len(title) == 0:
                logging.info("Title should not be empty")
                raise TypeError("Title should not be empty")
            if len(title) > 255:
                logging.info("Title should be under 255 characters")
                raise ValueError("Title should be under 255 characters")
            event.title = title

            #TODO: Implement some checks for description?
            event.description = description
            event.extended_description = extended_description

            if location is None or len(location) == 0:
                logging.info("Location should not be empty")
                raise TypeError("Location should not be empty")
            if len(location) > 255:
                logging.info("Location should be under 255 characters")
                raise ValueError("Location should be under 255 characters")
            event.location = location

            db.session.commit()
            try:
                valid_times = self.helper_valid_times(start_time, end_time)
            except Exception as e:
                raise ValueError(e)
            
            if valid_times:
                event.start_time = start_time
                event.end_time = end_time
            db.session.commit()


            # temp_start_datetime = None
            # temp_end_datetime = None

            # if start_time is not None:
            #     try: 
            #         temp_start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            #     except ValueError as e:
            #         logging.info(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")
            #         raise ValueError(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")

            # if end_time is not None:
            #     try: 
            #         temp_end_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            #     except ValueError as e:
            #         logging.info(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")
            #         raise ValueError(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")

            # if temp_end_datetime < temp_start_datetime:
            #     logging.info("Start time should be after end time")
            #     raise ValueError("Start time should be after end time")
            
            # if temp_start_datetime is not None:
            #     logging.warning(type(temp_start_datetime))
            #     event.start_time = temp_start_datetime
            # if temp_end_datetime is not None:
            #     logging.warning(type(temp_start_datetime))
            #     event.end_time = temp_end_datetime
            
            db.session.commit()

        # with app.app_context():
        #     author = User.query.filter_by(username=author_name).first()
        # if author is None:
        #     logging.info(f"Username {author_name} unable to post")
        #     raise TypeError(f"Username {author_name} unable to post")
        # event.author_id = author.id
        
        # if is_published is None:
        #     logging.info("Event was not published")
        #     raise TypeError("Event was not published")
        # event.is_published = is_published

    def get_all_events(self):
        with app.app_context():
            events = Event.query.all()
            return events
        
    def get_event_by_id(self, id):
        with app.app_context():
            event = Event.query.filter_by(id=id).first()
            if event is None:
                logging.info(f"Event with id {id} does not exist")
                raise ValueError(f"Event with id {id} does not exist")
            return event
        
    def get_tags_for_event(self, event_id):
        '''
        Returns a list of Tag objects that are associated with the given event id. 
        '''
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if event.tags == None:
                return []
            return event.tags
    
    def delete_event_by_id(self, event_id):
        '''
        Deletes the event with the given event id. 
        '''
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if event is None:
                logging.info(f"Event with id {event_id} {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event with id {event_id} {self.DOES_NOT_EXIST}")
            db.session.delete(event)
            db.session.commit()