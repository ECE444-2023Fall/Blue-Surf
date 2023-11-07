from backend.app import app, db
from backend.models import User, Event, Tag, UserInterestedEvent, EventTag


with app.app_context():
    # create the database and the db table
    db.create_all()

    # commit the changes
    db.session.commit()