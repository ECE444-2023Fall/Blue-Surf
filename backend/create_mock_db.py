# create_db.py
import os
from app import app, db
from models import User, Event, Tag, Like
from datetime import datetime

def create_mock_users():
    users = [
        User(
            username="Sarah Hudson",
            email="sarah@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        ),
        User(
            username="Ahmed Khan",
            email="ahmed@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        ),
        User(
            username="Alex Smith",
            email="alex@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        ),
    ]
    return users

def create_mock_user_events():
    user_events = [
        Like(
            user_id=1,
            event_id=1
        ),
        Like(
            user_id=1,
            event_id=2
        ),
        Like(
            user_id=3,
            event_id=3
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
            description="Meet top recruiters from leading companies.",
            extended_description="The Fall Career Week is a premier event that offers a unique platform for students and recent graduates to connect with recruiters from top firms across the nation. Attendees will have the chance to network, learn about job opportunities, and gain insights into various industries. This event is perfect for those looking to start or advance their careers.",
            location="online",
            start_time=start_time,
            end_time=end_time,
            author_id=1,
            is_published=True,
            like_count=0,
            club="YNCN, You're Next Career Networks",
            image=image_data
        ),
        ["Career Development"]),
        (Event(
            title="Origami Workshop",
            description="Discover the joy of paper folding.",
            extended_description="Our Origami Workshop is designed for both beginners and those with some experience in the art of paper folding. Participants will learn the basic folds and techniques required to create beautiful origami models. From classic cranes to intricate flowers, the workshop provides a relaxing and rewarding experience for everyone involved.",
            location="Bahen 8th Floor",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=10,
            club="Origami club",
            image=image_data
        ),[]),
        (Event(
            title="Community Soccer Match",
            description="Join us for a friendly soccer match.",
            extended_description="The community soccer match is a weekly event that invites players of all skill levels to enjoy a fun and competitive game. It's a fantastic opportunity to stay active, meet new friends, and indulge in the love of the sport. Whether you're an experienced player or just looking to kick the ball around, the event is open to everyone.",
            location="Varsity Stadium",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=5,
            club="Skule Soccer",
            image=image_data
        ),[]),
        (Event(
            title="Hockey Game",
            description="Come watch our varsity team play.",
            extended_description="Join us at the Varisty Arena to watch our varsity hockey team play against Waterloo",
            location="Varsity Arena",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=10,
            image=image_data
        ),
        ["Clubs & Organizations", "Arts & Culture"]),
        (Event(
            title="Spanish Lessons",
            description="Want to learn Spanish? Join our club.",
            extended_description="The spanish lesson meetup is a weekly event that invites non native spanish speakers to learn.",
            location="Bahen",
            start_time=start_time,
            end_time=end_time,
            author_id=None,
            is_published=True,
            like_count=5,
            club="Lesa",
            image=image_data
        ),[]),
        (Event(
            title="Skateboard Contest",
            description="Compete or just have fun at our skateboard contest.",
            extended_description="Our annual skateboard contest is back, bigger and better than ever. Skateboarders from all over the city will come together to showcase their skills and compete for prizes. With categories for different age groups and skill levels, everyone from novices to pros can participate. Even if you're not competing, come enjoy the vibrant atmosphere and cheer on your favorite skaters.",
            location="Galbraith",
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
    for (event, tag_names) in events:
        db.session.add(event)
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag:
                event.tags.append(tag)
        
    user_events = create_mock_user_events()
    for user_event in user_events: 
        db.session.add(user_event)
    
    # commit the changes
    db.session.commit()
