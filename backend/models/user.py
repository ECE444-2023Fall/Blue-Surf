from app import db

class User(db.Model):
    """
    This is the PostgreSQL database schema for the User table.
    
    A note on Password Hash vs. Password Salt: When a user creates an account or
    changes their password, the application should generate a new random salt,
    combine it with the user's chosen password, and hash the result before
    storing it in the password_hash column. Then, during login, the application
    should retrieve the salt associated with the user and perform the same
    hashing process on the entered password, then compare the resulting hash
    with the stored hash in the database to authenticate the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    password_salt = db.Column(db.String(255), nullable=False)
    user_profile_created = db.Column(db.Boolean, nullable=False, default=False)
    
    # Define a one-to-many relationship with events authored by the user
    events_authored = db.relationship('Event', backref='author', lazy=True)

    # Define a many-to-many relationship with events the user is interested in
    events_interested = db.relationship('Event', secondary='user_interested_event', backref='interested_users', lazy=True)