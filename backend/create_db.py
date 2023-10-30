# create_db.py
import os
from app import app, db
from models import User, Event, Tag, UserInterestedEvent, EventTag
from datetime import datetime

def create_mock_users():
    users = [
        User(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
            user_profile_created=True,
        ),
        User(
            username="testuser2",
            email="testuser2@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
            user_profile_created=True,
        ),
        User(
            username="testuser3",
            email="testuser3@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
            user_profile_created=True,
        ),
    ]
    return users

def create_mock_events():
    start_time = datetime.strptime("2023-10-28 09:00:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2023-10-28 11:00:00", "%Y-%m-%d %H:%M:%S")
    
    # Read the image file
    image_file_path = os.path.join("../images", "logo.png")
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()
        
    events = [
        Event(
            title="Test Event1",
            description="Test Event Description1",
            start_time=start_time,
            end_time=end_time,
            author_id=1, # Author of this event is user 1 (id = 1).
            is_published=True,
            like_count=0,
            image=image_data
        ),
        Event(
            title="Test Event2",
            description="Test Event Description2",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=5,
            image=image_data
        ),
        Event(
            title="Test Event3",
            description="Test Event Description3",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=10,
            image=image_data
        ),
    ]
    return events
    
    
with app.app_context():
    # create the database and the db table
    db.drop_all()
    db.create_all()
    
    users = create_mock_users()
    for user in users: 
        db.session.add(user)
        
    events = create_mock_events()
    for event in events:
        db.session.add(event)

    # commit the changes
    
    db.session.commit()
    user_to_delete = User.query.filter_by(username='testuser1').first()
    if user_to_delete:
        # Delete the user
        db.session.delete(user_to_delete)
        
    db.session.commit()