from app import app, db
from models import User
from datalayer_abstract import DataLayer
import logging

'''
class User:
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

class UserDataLayer(DataLayer):
    def create_user(self, username, email, password_hash, password_salt):
        user = User()

        if username is None or len(username) == 0:
            logging.info(f"Username {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Username {self.SHOULD_NOT_BE_EMPTY}")
        with app.app_context():
            user_exists = User.query.filter_by(username=username).first()
        if user_exists is not None:
            logging.info(f"Username {username} exists")
            raise ValueError(f"Username {username} {self.ALREADY_EXISTS}")
        if len(username) > 255:
            logging.info(f"Username {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
            raise ValueError(f"Username {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
        user.username = username 

        if email is None or len(email) == 0:
            logging.info(f"Email {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Email {self.SHOULD_NOT_BE_EMPTY}")
        with app.app_context():
            email_exists = User.query.filter_by(email=email).first()
        if email_exists is not None:
            logging.info(f"Email {email} {self.ALREADY_EXISTS}")
            raise ValueError(f"Email {email} {self.ALREADY_EXISTS}")
        if len(email) > 255:
            logging.info(f"Email {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}") 
            raise ValueError(f"Email {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}") 
        user.email = email

        #TODO: Come back to this for the password hashing algorithm/authentication.
        if password_hash is None or len(password_hash) == 0:
            logging.info(f"Password_hash {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Password_hash {self.SHOULD_NOT_BE_EMPTY}")
        if len(password_hash) > 255:
            logging.info(f"Password_hash {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")  
            raise ValueError(f"Password_hash {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}") 
        user.password_hash = password_hash
        
        #TODO: Come back to this for the password hashing algorithm/authentication.
        if password_salt is None or len(password_salt) == 0:
            logging.info(f"Password_salt {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Password_salt {self.SHOULD_NOT_BE_EMPTY}")
        if len(password_salt) > 255:
            logging.info(f"Password_salt {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")  
            raise ValueError(f"Password_salt {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}") 
        user.password_salt = password_salt
        
        with app.app_context():
            db.session.add(user)
            db.session.commit() 


