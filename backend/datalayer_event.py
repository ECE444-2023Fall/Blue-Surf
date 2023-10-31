import os
from app import app, db
from models import User, Event, Tag, UserInterestedEvent, EventTag
from datetime import datetime
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
            logging.info("Title should not be emtpy")
            raise TypeError("Title should not be emtpy")
        if len(title) > 255:
            logging.info("Title should be under 255 characters")
            raise ValueError("Title should be under 255 characters")
        event.title = title

        #TODO: Implement some checks for description?
        event.description = description

        # Setting the event location
        if len(location) > 255:
            logging.info("Location should be under 255 characters")
            raise ValueError("Location should be under 255 characters")
        event.location = location

        if start_time is None:
            logging.info("Start time should not be emtpy")
            raise TypeError("Start time should not be emtpy")
        try: 
            temp_start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info('Start time is not given in correct format')
        event.start_time = temp_start_datetime

        if end_time is None:
            logging.info("End time should not be emtpy")
            raise TypeError("End time should not be emtpy")
        try: 
            temp_end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info('End time is not given in correct format')
        event.start_time = temp_end_datetime

        with app.app_context():
            author = User.query.filter_by(username=author_name).first()
        if author is None:
            logging.info(f"Username {author} unable to post")
            raise ValueError(f"Username {author } unable to post")
        event.author_id = author.id
        
        if is_published is None:
            logging.info("Event was not published")
            raise TypeError("Event was not published")
        event.is_published = is_published

        with app.app_context():
            db.session.add(event)
            db.session.commit()


