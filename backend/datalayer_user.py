from app import app, db
from models import User
from datalayer_abstract import DataLayer
import logging

'''
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    password_salt = db.Column(db.Text, nullable=False)

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
    '''
    The UserDataLayer should be accessed by the rest of the code when trying to access the User table in the database.
    '''
    def create_user(self, username, email, password_hash, password_salt):
        '''
        Create user validates the input before adding a new user to the database.
        It checks for null fields, duplicate entries, and fields that exceed their character limit.
        Expect TypeError or ValueError to be raised when calling this function, so use it in a try/except block.
        '''
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

    def get_user(self, user_identifier):
        with app.app_context():
            user = User.query.filter_by(username=user_identifier).first()
            if user is not None:
                return user
            user = User.query.filter_by(email=user_identifier).first()
            if user is not None:
                return user
            logging.info(f"User with username/email {user_identifier} {self.DOES_NOT_EXIST}")
            raise ValueError(f"User with username/email {user_identifier} {self.DOES_NOT_EXIST}")


