from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'NEED TO CHANGE'
# SQLite
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bluesurf.db'
# PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ncuhktvhlxcvlz:60726df95007500597f9e6f5a2b261a8a25bc456736f82d29778743e5c90c649@ec2-44-213-228-107.compute-1.amazonaws.com:5432/d4cqob0s0vcv6f'
# Initialize DB
db = SQLAlchemy(app)

# Create Model
class User(db.Model):
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

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    like_count = db.Column(db.Integer, default=0)

class UserInterestedEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def signup():
    return render_template('register.html')