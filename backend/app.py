from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


    
app = Flask(__name__)

app.config["SECRET_KEY"] = "NEED TO CHANGE"

# SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bluesurf.db"
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