import os
from pathlib import Path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = Path(__file__).resolve().parent

# configuration
DATABASE = "bluesurf-postgres.db"
SECRET_KEY = "NEED TO CHANGE"

url = os.getenv('DATABASE_URL', f'sqlite:///{Path(basedir).joinpath(DATABASE)}')

if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = url
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)
bootstrap = Bootstrap(app)

# Initialize DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .api import setup_routes
setup_routes(app)

from .create_mock_db import populate_database
populate_database(app, db)

if __name__ == "__main__":
    app.run()