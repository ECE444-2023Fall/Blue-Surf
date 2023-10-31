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
    def create_event(self,id, title, description, location, start_time, end_time, author_name, is_published, image):
        event = Event()

        # Setting the event title
        if title is not None:
            if len(title) < 256:
                event.title = title
            else:
                logging.info('Title is too long. Characters exceed 255.')
        else:
            logging.info('Title is empty')

        # Setting the event description
        event.description = description

        # Setting the event location
        if len(location) < 256:
                event.location = location
        else:
            logging.info('Location is too long. Characters exceed 255.')

        # Setting the event start_time
        if start_time is not None:
            try: 
                temp_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                logging.info('Start time is not given in correct format')
            event.start_time = datetime.strptime(temp_datetime, "%Y-%m-%d %H:%M:%S")
        else: 
            logging.info('Start time is empty')

        # Setting the event end time
        if end_time is not None:
            try: 
                temp_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                logging.info('End time is not given in correct format')
            event.end_time = datetime.strptime(temp_datetime, "%Y-%m-%d %H:%M:%S")
        else:
            logging.info('End time is empty')

        # Setting the event author_id
        author = User.query.filter_by(username=author_name).first()
        if author is not None:
            event.author_id = author.id
        
        # Setting the event published state
        if is_published is not None:
            event.is_published = is_published
        else: 
            logging.info('Event is not published')

        with app.app_context():
            db.session.add(event)
            db.session.commit()


