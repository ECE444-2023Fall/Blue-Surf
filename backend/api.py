from flask import jsonify, request, redirect, render_template
from urllib.parse import quote_plus
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)
import json
import bcrypt

# from datalayer_event import EventDataLayer


def get_matched_events(query, detailed=False):
    if not query:
        return []

    # Once database is setup, a query will be executed here
    matched_events = [
        event
        for event in mockEvents
        if event["title"].lower().startswith(query.lower())
    ]

    if detailed:
        return matched_events
    else:
        titles = [event["title"] for event in matched_events]
        return titles


def setup_routes(app):
    @app.errorhandler(404)
    def handle_404(e):
        if request.method == 'GET':
            return redirect(f'/?request_path={quote_plus(request.path)}')
        return e
    

    @app.route("/api/get-all-tags", methods=["GET"])
    def get_all_tags():
        try:
            from .datalayer.tag import TagDataLayer
            tag_data = TagDataLayer()
            tags = tag_data.get_all_tags()
            return jsonify(tags)
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to get all tags", "error message": error_message}
                ),
                500,
            )

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

    @app.route("/api/update-post/<int:post_id>", methods=["POST"])
    def update_post(post_id):
        try:
            # Retrieve the updated post data from the request
            updated_post = request.get_json()
            print(updated_post)

            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            event_data.update_event(
                event_id=post_id,
                title=updated_post["title"],
                description=updated_post["description"],
                extended_description=updated_post["extended_description"],
                location=updated_post["location"],
            )

            return jsonify({"message": "Post updated successfully"})
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to update post", "error message": error_message}
                ),
                500,
            )

    @app.route("/api/create-post", methods=["POST"])
    def create_post():
        try:
            # Retrieve the updated post data from the request
            new_post = request.get_json()

            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            event_data.create_event(
                title=new_post["title"],
                description=new_post["description"],
                extended_description=new_post["extended_description"],
                location=new_post["location"],
                start_time=new_post["start_time"],
                end_time=new_post["end_time"],
                author_name="Sarah Hudson",  # TODO: Needs to be changed to actual author
                is_published=True,
                club=new_post["club"],
                image=None,
                tags=new_post["tags"],
            )

            return jsonify({"message": "Post created successfully"})
        except TypeError as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to create post", "error message": error_message}
                ),
                400,
            )
        except ValueError as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to create post", "error message": error_message}
                ),
                400,
            )
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to process reqquest",
                        "error message": error_message,
                    }
                ),
                500,
            )

    @app.route("/api/", methods=["GET"])
    def index():
        try:
            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            events = event_data.get_all_events()

            json_events = []

            for event in events:
                tags = event_data.get_tags_for_event(event_id=event.id)
                tag_names = [tag.name for tag in tags]

                json_event = {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "extended_description": event.extended_description,
                    "location": event.location,
                    "start_time": event.start_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),  # Convert to string
                    "end_time": event.end_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),  # Convert to string
                    "author_id": event.author_id,
                    "club": event.club,
                    "is_published": event.is_published,
                    "like_count": event.like_count,
                    "tags": tag_names,
                    # Add other fields here as needed
                }

                json_events.append(json_event)

            return jsonify(json_events)
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to get all events",
                        "error message": error_message,
                    }
                ),
                500,
            )

    @app.route("/api/<int:event_id>", methods=["GET"])
    def get_event(event_id):
        try:
            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            event = event_data.get_event_by_id(event_id)

            tags = event_data.get_tags_for_event(event_id=event.id)
            tag_names = [tag.name for tag in tags]

            json_event = {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "extended_description": event.extended_description,
                "location": event.location,
                "start_time": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "author_id": event.author_id,
                "club": event.club,
                "is_published": event.is_published,
                "like_count": event.like_count,
                "tags": tag_names,
            }

            return jsonify(json_event)
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to get event", "error message": error_message}
                ),
                500,
            )

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

    @app.route("/api/token", methods=["POST"])
    def create_token():
        try:
            user_identifier = request.json.get("user_identifier", None)
            password = request.json.get("password", None)

            from .datalayer.user import UserDataLayer

            user_data = UserDataLayer()
            stored_user = user_data.get_user(user_identifier=user_identifier)
            stored_password_hash = stored_user.password_hash
            stored_password_salt = stored_user.password_salt

            entered_password_hash = bcrypt.hashpw(
                password.encode("utf-8"), stored_password_salt.encode("utf-8")
            ).decode("utf-8")

            if entered_password_hash == stored_password_hash:
                access_token = create_access_token(identity=stored_user.id)
                response = {
                    "access_token": access_token,
                    "id": stored_user.id,
                    "username": stored_user.username,
                }
                return response
            else:
                return (
                    jsonify(
                        {
                            "error": "Failed to login",
                            "error message": "Incorrect password.",
                        }
                    ),
                    401,
                )
        except ValueError as e:
            error_message = str(e)
            return (
                jsonify({"error": "Failed to login", "error message": error_message}),
                404,
            )
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to process the request",
                        "error message": error_message,
                    }
                ),
                500,
            )

    @app.route("/api/logout", methods=["POST"])
    def logout():
        try:
            response = jsonify({"msg": "logout successful"})
            unset_jwt_cookies(response)
            return response
        except Exception as e:
            error_message = str(e)
            return (
                jsonify({"error": "Failed to logout", "error message": error_message}),
                500,
            )

    @app.route("/api/register", methods=["POST"])
    def signup():
        try:
            username = request.json.get("username", None)
            email = request.json.get("email", None)
            password = request.json.get("password", None)

            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
                "utf-8"
            )

            from .datalayer.user import UserDataLayer

            user_data = UserDataLayer()
            user_data.create_user(
                username=username,
                email=email,
                password_hash=password_hash,
                password_salt=salt.decode("utf-8"),
            )

            return jsonify({"message": "User created successfully"})
        except TypeError as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to create user", "error message": error_message}
                ),
                400,
            )
        except ValueError as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to create user", "error message": error_message}
                ),
                400,
            )
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to process the request",
                        "error message": error_message,
                    }
                ),
                500,
            )

    @app.route("/api/dashboard")
    @jwt_required()  # new line
    def my_profile():
        # Call get_jwt_identity() to fetch userid for the logged-in user

        # Replace with db query that will fetch data based on the userid
        response_body = {
            "name": "Nagato",
            "about": "Hello! I'm a full stack developer that loves python and javascript",
        }

        return response_body


# TODO: Remove once database is setup
# TODO: add extendedDescription field, image url,
mockEvents = [
    {
        "event_id": 0,
        "title": "Sample Event 0",
        "description": "This is the first sample event.",
        "location": "Sample Location 1",
        "start_time": "2023-11-01T08:00:00",
        "end_time": "2023-11-01T17:00:00",
        "user_id": 1,
        "is_published": True,
        "is_public": True,
        "like_count": 25,
    },
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
        "like_count": 25,
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
        "like_count": 10,
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
        "like_count": 30,
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
        "like_count": 75,
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
        "like_count": 120,
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
        "like_count": 40,
    },
]
