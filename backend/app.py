from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import json
#from models import User
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["JWT_SECRET_KEY"] = "NEED TO CHANGE"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bluesurf.db"
#configure flask application instance 
jwt = JWTManager(app)
# PostgreSQL database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ncuhktvhlxcvlz:60726df95007500597f9e6f5a2b261a8a25bc456736f82d29778743e5c90c649@ec2-44-213-228-107.compute-1.amazonaws.com:5432/d4cqob0s0vcv6f'

# Initialize DB
db = SQLAlchemy(app)

def get_matched_events(query, detailed=False):
    if not query:
        return []
    
    # Once database is setup, a query will be executed here
    matched_events = [event for event in mockEvents if event['title'].lower().startswith(query.lower())]

    if detailed:
        return matched_events
    else:
        titles = [event['title'] for event in matched_events]
        return titles


@app.route("/api/autosuggest", methods=["GET"])
def autosuggest():
    query = request.args.get("query")
    results = get_matched_events(query)
    return jsonify(results)

@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query")
    results = get_matched_events(query, detailed=True)
    return jsonify(results)

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test" or password != "test":
        return {"msg": "Wrong email or password"}, 401

    access_token = create_access_token(identity=email)
    response = {"access_token":access_token}
    return response

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route('/profile')
@jwt_required() #new line
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body



# TODO: Remove once database is setup
mockEvents = [
  {
    "event_id": 1,
    "title": "Sample Event 1",
    "description": "This is the first sample event.",
    "location": "Sample Location 1",
    "start_time": "2023-11-01T08:00:00",
    "end_time": "2023-11-01T17:00:00",
    "user_id": 1,
    "is_published": True,
    "is_public": True,
    "like_count": 25
  },
  {
    "event_id": 2,
    "title": "Sample Event 2",
    "description": "A different kind of event.",
    "location": "Sample Location 2",
    "start_time": "2023-11-05T10:00:00",
    "end_time": "2023-11-05T16:00:00",
    "user_id": 2,
    "is_published": True,
    "is_public": True,
    "like_count": 10
  },
  {
    "event_id": 3,
    "title": "Another Event",
    "description": "Details about another event.",
    "location": "Sample Location 3",
    "start_time": "2023-11-10T12:00:00",
    "end_time": "2023-11-10T20:00:00",
    "user_id": 1,
    "is_published": True,
    "is_public": True,
    "like_count": 30
  },
  {
    "event_id": 4,
    "title": "Tech Conference 2023",
    "description": "Join us for the latest in tech trends.",
    "location": "Convention Center",
    "start_time": "2023-11-15T09:00:00",
    "end_time": "2023-11-17T18:00:00",
    "user_id": 3,
    "is_published": True,
    "is_public": True,
    "like_count": 75
  },
  {
    "event_id": 5,
    "title": "Music Festival",
    "description": "A three-day music extravaganza.",
    "location": "Outdoor Arena",
    "start_time": "2023-11-20T16:00:00",
    "end_time": "2023-11-22T23:00:00",
    "user_id": 2,
    "is_published": True,
    "is_public": True,
    "like_count": 120
  },
  {
    "event_id": 6,
    "title": "Local Charity Run",
    "description": "Support a good cause while staying fit.",
    "location": "City Park",
    "start_time": "2023-11-25T07:30:00",
    "end_time": "2023-11-25T11:00:00",
    "user_id": 4,
    "is_published": True,
    "is_public": True,
    "like_count": 40
  }
]