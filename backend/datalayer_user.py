import os
from app import app, db
from models import User, Event, Tag, UserInterestedEvent, EventTag
from datetime import datetime
import logging

'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    password_salt = db.Column(db.String(255), nullable=False)

    # Define a one-to-many relationship with events authored by the user
    events_authored = db.relationship("Event", backref="author", lazy=True)

    # Define a many-to-many relationship with events the user is interested in
    events_interested = db.relationship(
        "Event",
        secondary="user_interested_event",
        backref="interested_users",
        lazy=True,
    )
'''

class UserDataLayer():
    def create_user(self, username, email, password_hash, password_salt):
        user = User()

        if username is None or len(username) == 0:
            logging.info('Username is empty')
            raise TypeError("Username should not be empty")
        with app.app_context():
            user_exists = User.query.filter_by(username=username).first()
        if user_exists is not None:
            logging.info(f"Username {username} exists")
            raise ValueError(f"Username {username } already exists")
        if len(username) > 255:
            logging.info("Username too long")
            raise ValueError("Username should be under 255 characters")
        user.username = username 

        if email is None or len(email) == 0:
            logging.info("Email is empty")
            raise TypeError("Email should not be empty")
        with app.app_context():
            email_exists = User.query.filter_by(email=email).first()
        if email_exists is not None:
            logging.info(f"Email {email} exists")
            raise ValueError(f"Email {email} already exists")
        if len(email) > 255:
            logging.info("Email too long") 
            raise ValueError("Email should be under 255 characters") 
        user.email = email

        #TODO: Come back to this for the password hashing algorithm/authentication.
        if password_hash is None:
            logging.info('Password_hash is empty')
            raise TypeError("Password_hash should not be empty")
        if len(password_hash) > 255:
            logging.info('Password_hash too long')  
            raise ValueError("Password_hash should be under 255 characters") 
        user.password_hash = password_hash
        
        #TODO: Come back to this for the password hashing algorithm/authentication.
        if password_salt is None:
            logging.info('Password_salt is empty')
            raise TypeError("Password_salt should not be empty")
        if len(password_salt) > 255:
            logging.info('Password_salt too long')  
            raise ValueError("Password_salt should be under 255 characters") 
        user.password_salt = password_salt
        
        with app.app_context():
            db.session.add(user)
            db.session.commit() 


