import os
from app import app, db
from models import User, Event, Tag, UserInterestedEvent, EventTag
from datetime import datetime
from flask import jsonify
import logging

'''
    class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    like_count = db.Column(db.Integer, default=0)
    image = db.Column(db.LargeBinary, nullable=True)
'''

class EventDataLayer():
    def create_event(self, title, description, location, start_time, end_time, author_name, is_published, image):
        event = Event()

        if title is None or len(title) == 0:
            logging.info("Title should not be empty")
            raise TypeError("Title should not be empty")
        if len(title) > 255:
            logging.info("Title should be under 255 characters")
            raise ValueError("Title should be under 255 characters")
        event.title = title

        #TODO: Implement some checks for description?
        event.description = description

        if location is None or len(location) == 0:
            logging.info("Location should not be empty")
            raise TypeError("Location should not be empty")
        if len(location) > 255:
            logging.info("Location should be under 255 characters")
            raise ValueError("Location should be under 255 characters")
        event.location = location

        if start_time is None:
            logging.info("Start time should not be empty")
            raise TypeError("Start time should not be empty")
        try: 
            temp_start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info("Start time is not given in correct format")
            raise ValueError("Start time is not given in correct format")

        if end_time is None:
            logging.info("End time should not be empty")
            raise TypeError("End time should not be empty")
        try: 
            temp_end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info("End time is not given in correct format")
            raise ValueError("End time is not given in correct format")

        if temp_end_datetime < temp_start_datetime:
            logging.info("Start time should be after end time")
            raise ValueError("Start time should be after end time")
        event.start_time = temp_start_datetime
        event.end_time = temp_end_datetime

        with app.app_context():
            author = User.query.filter_by(username=author_name).first()
        if author is None:
            logging.info(f"Username {author_name} unable to post")
            raise TypeError(f"Username {author_name} unable to post")
        event.author_id = author.id
        
        if is_published is None:
            logging.info("Event was not published")
            raise TypeError("Event was not published")
        event.is_published = is_published

        with app.app_context():
            db.session.add(event)
            db.session.commit()

    def update_event(self, event_id, title, description, location, image=None, is_published=True, start_time=None, end_time=None):
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

            if location is None or len(location) == 0:
                logging.info("Location should not be empty")
                raise TypeError("Location should not be empty")
            if len(location) > 255:
                logging.info("Location should be under 255 characters")
                raise ValueError("Location should be under 255 characters")
            event.location = location

            db.session.commit()

        # if start_time is None:
        #     logging.info("Start time should not be empty")
        #     raise TypeError("Start time should not be empty")
        # try: 
        #     temp_start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        # except ValueError:
        #     logging.info("Start time is not given in correct format")
        #     raise ValueError("Start time is not given in correct format")

        # if end_time is None:
        #     logging.info("End time should not be empty")
        #     raise TypeError("End time should not be empty")
        # try: 
        #     temp_end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        # except ValueError:
        #     logging.info("End time is not given in correct format")
        #     raise ValueError("End time is not given in correct format")

        # if temp_end_datetime < temp_start_datetime:
        #     logging.info("Start time should be after end time")
        #     raise ValueError("Start time should be after end time")
        # event.start_time = temp_start_datetime
        # event.end_time = temp_end_datetime

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


            


