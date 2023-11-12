from flask import jsonify, request
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
import re

"""
Helper Methods 
"""


def jsonify_event(event):
    """
    Returns a json string of a single event
    """
    from datalayer_event import EventDataLayer

    event_data = EventDataLayer()
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
        "end_time": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),  # Convert to string
        "author_id": event.author_id,
        "club": event.club,
        "is_published": event.is_published,
        "like_count": event.like_count,
        "tags": tag_names,
        # Add other fields here as needed
    }
    return json_event


def jsonify_event_list(events):
    """
    Returns a json string of a list of events
    """
    json_events = []
    for event in events:
        json_event = jsonify_event(event)
        json_events.append(json_event)
    return jsonify(json_events)


"""
Routes
"""


def setup_routes(app):
    @app.route("/api/get-all-tags", methods=["GET"])
    def get_all_tags():
        try:
            from datalayer_tag import TagDataLayer

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
    
    @app.route("/api/get-all-locations", methods=["GET"])
    def get_all_locations():
        try:
            from datalayer_event import EventDataLayer
            
            event_data = EventDataLayer()
            locations = event_data.get_all_locations()
            return jsonify(locations)
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to get all locations", "error message": error_message}
                ),
                500,
            )
        
    @app.route("/api/get-all-clubs", methods=["GET"])
    def get_all_clubs():
        try:
            from datalayer_event import EventDataLayer
            
            event_data = EventDataLayer()
            clubs = event_data.get_all_clubs()
            return jsonify(clubs)   
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to get all clubs", "error message": error_message}
                ),
                500,
            )

    @app.route("/api/autosuggest", methods=["GET"])
    def autosuggest():
        query = request.args.get("query").lower()
        print("query: ", query)
        try:
            from datalayer_event import EventDataLayer

            event_data = EventDataLayer()
            results = event_data.get_search_results_by_keyword(query)
            suggestions = []
            for event in results:
                if any(
                    word.lower().startswith(query)
                    for word in re.findall(r"\b\w+\b", event.title)
                ):
                    suggestions.append(event.title)
                if event.club and any(
                    word.lower().startswith(query)
                    for word in re.findall(r"\b\w+\b", event.club)
                ):
                    suggestions.append(event.club)
            return jsonify(list(set(suggestions)))
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to look and display post title",
                        "error_message": error_message,
                    }
                ),
                500,
            )

    @app.route("/api/search", methods=["GET"])
    def search():
        query = request.args.get("query")
        print("Printing query: ", query)
        try:
            from datalayer_event import EventDataLayer

            event_data = EventDataLayer()
            events = event_data.get_search_results_by_keyword(query)
            return jsonify_event_list(events)
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to look for post", "error_message": error_message}
                ),
                500,
            )

    @app.route("/api/update-post/<int:post_id>", methods=["POST"])
    def update_post(post_id):
        try:
            # Retrieve the updated post data from the request
            updated_post = request.get_json()
            print(updated_post)

            from datalayer_event import EventDataLayer

            event_data = EventDataLayer()
            event_data.update_event(
                event_id=post_id,
                title=updated_post["title"],
                description=updated_post["description"],
                extended_description=updated_post["extended_description"],
                location=updated_post["location"],
                tags=updated_post["tags"],
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

            from datalayer_event import EventDataLayer

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
            from datalayer_event import EventDataLayer

            event_data = EventDataLayer()
            events = event_data.get_all_events()

            return jsonify_event_list(events)

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
        from datalayer_event import EventDataLayer
        from datalayer_tag import TagDataLayer

        try:
            event_data = EventDataLayer()
            event = event_data.get_event_by_id(event_id)
            return jsonify_event(event)
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

            from datalayer_user import UserDataLayer

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

            from datalayer_user import UserDataLayer

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
        try:
            # Call get_jwt_identity() to fetch userid for the logged-in user
            userid = get_jwt_identity()
            print("userid: " + str(userid))
            from datalayer_event import EventDataLayer

            event_data = EventDataLayer()
            events = event_data.get_authored_events(userid)
            return jsonify_event_list(events)

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

    @app.route("/api/filter", methods=["GET"])
    def filter_tags():
        try:
            from datalayer_event import EventDataLayer

            event_data = EventDataLayer()

            # start by getting the search results
            query = request.args.get("query", default="").lower()
            tagname = request.args.get("tag", None)
            location = request.args.get("location", None)
            club = request.args.get("club", None)
            start_time = request.args.get("start_time", None)
            end_time = request.args.get("end_time", None)
            sortby = request.args.get("sortby", None)
            events = event_data.search_filter_sort(keyword=query, tag_name=tagname, location=location, club=club, start_time=start_time, end_time=end_time, sort_by=sortby)

            return jsonify_event_list(events)
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to search sort and filter events",
                        "error message": error_message,
                    }
                ),
                500,
            )

    @app.route("/api/like/<int:event_id>", methods=["POST"])
    @jwt_required()
    def like_post(event_id):
        try:
            user_id = get_jwt_identity()

            from datalayer_like import LikeLayer

            like_layer = LikeLayer()
            like_layer.like_by_id(user_id, event_id)

            return jsonify({"message": "Post liked successfully"})
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to like post", "error message": error_message}
                ),
                500,
            )

    @app.route("/api/unlike/<int:event_id>", methods=["POST"])
    @jwt_required()
    def unlike_post(event_id):
        try:
            user_id = get_jwt_identity()

            from datalayer_like import LikeLayer

            like_layer = LikeLayer()
            like_layer.unlike_by_id(user_id, event_id)

            return jsonify({"message": "Post unliked successfully"})
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to unlike post", "error message": error_message}
                ),
                500,
            )
