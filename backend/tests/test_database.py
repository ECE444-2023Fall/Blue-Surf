import sys
import pytest
from datetime import datetime

sys.path.append('../')
from app import app, db, User, Event, UserInterestedEvent

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/db/test_database.db'
    with app.app_context():
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        if 'sqlalchemy' not in app.extensions:
            db.init_app(app)
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_user_creation(test_client):
    user = User(username='testuser', email='testuser@example.com', password_hash='testpassword', password_salt='testpassword', user_profile_created=True)
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(username='testuser').first()
        assert retrieved_user.username == 'testuser'
        assert retrieved_user.email == 'testuser@example.com'
        assert retrieved_user.user_profile_created == True

def test_event_creation(test_client):
    start_time = datetime.strptime('2023-10-28 09:00:00', '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime('2023-10-28 11:00:00', '%Y-%m-%d %H:%M:%S')

    event = Event(
        title='Test Event',
        description='Test Event Description',
        start_time=start_time,
        end_time=end_time,
        author=None,
        is_published=True,
        like_count=0
    )
    with app.app_context():
        db.session.add(event)
        db.session.commit()
        retrieved_event = Event.query.filter_by(title='Test Event').first()
        assert retrieved_event.title == 'Test Event'
        assert retrieved_event.is_published == True
