from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os
from pathlib import Path


# from models import User
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["JWT_SECRET_KEY"] = "NEED TO CHANGE"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# SQLite
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bluesurf.db"
# configure flask application instance
jwt = JWTManager(app)

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = "bluesurf-postgresql"

url = os.getenv("DATABASE_URL", f"sqlite:///{Path(basedir).joinpath(DATABASE)}")
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
SQLALCHEMY_DATABASE_URI = url
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

bootstrap = Bootstrap(app)
# Initialize DB
db = SQLAlchemy(app)

from .api import setup_routes

setup_routes(app)

# Run populate_database only in development environment
if app.config.get("ENV") == "development" or app.config.get("ENV") == "testing":
    print("Populating database...")
    from .create_mock_db import populate_database

    populate_database(app, db)

if __name__ == "__main__":
    app.run()
