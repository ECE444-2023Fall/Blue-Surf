import os
import sys
import pytest
import logging

sys.path.append("../")
from app import app, db

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

    yield app.test_client()

    with app.app_context():
        db.session.remove()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        