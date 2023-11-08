import os
import pytest
import logging

from ..app import app, db
from ..models import User, Event, Tag, UserInterestedEvent

@pytest.fixture(scope="function")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tests/db/test_datalayer.db"

    # Get the directory of the current script
    current_dir = os.getcwd() 

    # Define the log file path
    log_file = os.path.join(current_dir, "test_logs.txt")
    logging.basicConfig(level=logging.DEBUG, filename=log_file)

    with app.app_context():
        if not hasattr(app, "extensions"):
            app.extensions = {}
        if "sqlalchemy" not in app.extensions:
            db.init_app(app)
        db.create_all()
        
        # Clear the tables
        db.session.execute(User.__table__.delete())
        db.session.execute(Event.__table__.delete())
        db.session.execute(Tag.__table__.delete())
        db.session.execute(UserInterestedEvent.__table__.delete())
        db.session.commit()

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        try:
            for table in reversed(db.metadata.sorted_tables):
                db.session.execute(table.delete())
            db.session.commit()
        except Exception as e:
            # Handle any exceptions that may occur during teardown
            logging.error(f"Teardown error: {str(e)}")
        
