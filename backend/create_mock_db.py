# create_db.py
import os
from app import app, db
from models import User, Event, Tag, UserInterestedEvent
from datetime import datetime

def create_mock_users():
    users = [
        User(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        ),
        User(
            username="testuser2",
            email="testuser2@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        ),
        User(
            username="testuser3",
            email="testuser3@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        ),
    ]
    return users

def create_mock_user_events():
    user_events = [
        UserInterestedEvent(
            user_id = 1,
            event_id = 1
        ),
        UserInterestedEvent(
            user_id = 1,
            event_id = 2
        ),
        UserInterestedEvent(
            user_id = 3,
            event_id = 3
        ),
    ]
    return user_events

def create_mock_events():
    start_time = datetime.strptime("2023-10-28 09:00:00", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime("2023-10-28 11:00:00", "%Y-%m-%d %H:%M:%S")
    
    # Read the image file
    image_file_path = os.path.join("../images", "logo.png")
    with open(image_file_path, "rb") as image_file:
        image_data = image_file.read()
        
    events = [
        (Event(
            title="Fall Career Week",
            description="Come out to the Fall Career Week to meet recruiters from companies like RBC, Tesla and more!",
            location="online",
            start_time=start_time,
            end_time=end_time,
            author_id=1, # Author of this event is user 1 (id = 1).
            is_published=True,
            like_count=0,
            image=image_data
        ),
        ["Career Developmment"]),
        (Event(
            title="Test Event2",
            description="Test Event Description2",
            location="online",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=5,
            image=image_data
        ),
        ["Academic"]),
        (Event(
            title="Test Event3",
            description="Test Event Description3",
            location="online",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=10,
            image=image_data
        ),
        ["Clubs & Organizations", "Arts & Culture"]),
    ]
    return events
    
def create_mock_tags():
    tags = [
        Tag(name="Academic"),
        Tag(name="Career Development"),
        Tag(name="Clubs & Organizations"),
        Tag(name="Arts & Culture"),
        Tag(name="Sports & Fitness"),
        Tag(name="Volunteering"),
        Tag(name="Social Events"),
        Tag(name="Science & Technology"),
        Tag(name="Health & Wellness"),
        Tag(name="Community Awareness"),
        Tag(name="Workshops & Seminars"),
        Tag(name="Conferences"),
        Tag(name="Food & Dining"),
        Tag(name="Entertainment"),
        Tag(name="Travel & Exploration"),
        Tag(name="Environmental Initiatives"),
        Tag(name="Music & Concerts"),
        Tag(name="Fashion & Style"),
        Tag(name="Tech Hackathons"),
        Tag(name="LGBTQ+ & Inclusivity")
    ]
    return tags

with app.app_context():
    # create the database and the db table
    db.drop_all()
    db.create_all()
    
    users = create_mock_users()
    for user in users: 
        db.session.add(user)

    tags = create_mock_tags()
    for tag in tags:
        db.session.add(tag)
        
    events = create_mock_events()
    for (event, tags) in events:
        db.session.add(event)
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is not None:
                event.tags.append(tag)
        
    user_events = create_mock_user_events()
    for user_event in user_events: 
        db.session.add(user_event)

    
    # commit the changes
    db.session.commit()