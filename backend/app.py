from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import json
#from models import User
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "NEED TO CHANGE"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bluesurf.db"
#configure flask application instance 
jwt = JWTManager(app)
# PostgreSQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ncuhktvhlxcvlz:60726df95007500597f9e6f5a2b261a8a25bc456736f82d29778743e5c90c649@ec2-44-213-228-107.compute-1.amazonaws.com:5432/d4cqob0s0vcv6f'

bootstrap = Bootstrap(app)
# Initialize DB
db = SQLAlchemy(app)

from .api import setup_routes
setup_routes(app)

from .create_mock_db import populate_database
populate_database(app, db)

if __name__ == "__main__":
    app.run()