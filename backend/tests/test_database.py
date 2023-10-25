import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, User, Event, EventAttendee, UserInterestedEvent
from datetime import datetime

class TestDatabase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
        self.app = app.test_client()
        with app.app_context():
            if not hasattr(app, 'extensions'):
                app.extensions = {}
            if 'sqlalchemy' not in app.extensions:
                db.init_app(app)
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        user = User(username='testuser', email='testuser@example.com', password='testpassword', user_profile_created=True)
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            retrieved_user = User.query.filter_by(username='testuser').first()
            self.assertEqual(retrieved_user.username, 'testuser')
            self.assertEqual(retrieved_user.email, 'testuser@example.com')
            self.assertTrue(retrieved_user.user_profile_created)

    # def test_event_creation(self):
    #     start_time = datetime.strptime('2023-10-28 09:00:00', '%Y-%m-%d %H:%M:%S')
    #     end_time = datetime.strptime('2023-10-28 11:00:00', '%Y-%m-%d %H:%M:%S')

    #     event = Event(
    #         title='Test Event',
    #         description='Test Event Description',
    #         start_time=start_time,
    #         end_time=end_time,
    #         author=None,  # You can set the author to a user if needed
    #         is_published=True,
    #         like_count=0
    #     )
    #     with app.app_context():
    #         db.session.add(event)
    #         db.session.commit()
    #         retrieved_event = Event.query.filter_by(title='Test Event').first()
    #         self.assertEqual(retrieved_event.title, 'Test Event')
    #         self.assertEqual(retrieved_event.is_published, True)


    def test_event_attendee_relationship(self):
        user = User(username='testuser', email='testuser@example.com', password='testpassword', user_profile_created=True)
        event = Event(
            title='Test Event',
            description='Test Event Description',
            start_time='2023-10-28 09:00:00',
            end_time='2023-10-28 11:00:00',
            author=None,  # You can set the author to a user if needed
            is_published=True,
            like_count=0
        )
        with app.app_context():
            db.session.add(user)
            db.session.add(event)
            db.session.commit()
            event.attendees.append(user)
            db.session.commit()
            retrieved_event = Event.query.filter_by(title='Test Event').first()
            self.assertEqual(len(retrieved_event.attendees), 1)
            self.assertEqual(retrieved_event.attendees[0].username, 'testuser')

if __name__ == '__main__':
    unittest.main()
