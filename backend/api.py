import base64
import io
from flask import jsonify, request, send_file, Response
import re

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
    from .datalayer.event import EventDataLayer

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
                    {
                        "error": "Failed to get all locations",
                        "error message": error_message,
                    }
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
            from .datalayer.event import EventDataLayer

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
            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            results = event_data.get_search_results_by_keyword(query)
            json_event = [
                {
                    "id": event.id,
                    "title": event.title,
                    "description": event.description,
                    "location": event.location,
                    "start_time": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_time": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for event in results
            ]
            return jsonify(json_event)
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

            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            event_data.update_event(
                event_id=post_id,
                title=updated_post["title"],
                description=updated_post["description"],
                extended_description=updated_post["extended_description"],
                location=updated_post["location"],
                tags=updated_post["tags"],
                # Need to add start date and time once added to the db#
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

    @app.route("/api/update-post-image/<int:post_id>", methods=["POST"])
    def update_post_image(post_id):
        try:
            # Check if the request contains a file in the 'image' field
            if "image" not in request.files:
                return jsonify({"error": "No image file provided"}), 400

            # Retrieve the image file from the request
            uploaded_file = request.files["image"]

            # Read the image file data
            image_data = uploaded_file.read()

            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            event_data.update_image(event_id=post_id, image=image_data)

            # THIS IS FOR TESTING PURPOSES ONLY
            # import io
            # from pathlib import Path
            # from PIL import Image

            # # Process the image data
            # image = Image.open(io.BytesIO(image_data))

            # # Save the received image for testing purposes
            # subdirectory_name = "output_images"
            # output_directory = Path.cwd() / subdirectory_name
            # output_directory.mkdir(parents=True, exist_ok=True)

            # output_image_path = output_directory / "received_image.png"
            # image.save(output_image_path)

            return jsonify({"message": "Image updated successfully"})

        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to update image", "error message": error_message}
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
            event_id = event_data.create_event(
                title=new_post["title"],
                description=new_post["description"],
                extended_description=new_post["extended_description"],
                location=new_post["location"],
                start_time=new_post["start_time"],
                end_time=new_post["end_time"],
                author_id=new_post[
                    "author_id"
                ],  # TODO: Needs to be changed to actual author
                is_published=True,
                club=new_post["club"],
                tags=new_post["tags"],
            )

            return jsonify({"message": "Post created successfully", "id": event_id})
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

    @app.route("/api/delete-post/<int:post_id>", methods=["POST"])
    @jwt_required()
    def delete_post(post_id):
        try:
            from .datalayer.event import EventDataLayer

            event_data = EventDataLayer()
            event_data.delete_event_by_id(
                id=post_id,
            )

            return jsonify({"message": "Post deleted successfully"})
        except ValueError as e:
            error_message = str(e)
            return (
                jsonify(
                    {"error": "Failed to delete post", "error message": error_message}
                ),
                404,
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
        from .datalayer.event import EventDataLayer

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

    @app.route("/api/<int:event_id>/image", methods=["GET"])
    def get_event_image(event_id):
        from .datalayer.event import EventDataLayer

        try:
            event_data = EventDataLayer()
            event = event_data.get_event_by_id(event_id)

            if event.image:
                # Assuming event.image is the binary image data
                return Response(event.image, mimetype="image/png")

            else:
                return jsonify({"error": "Image not found"})
        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to get event image",
                        "error message": error_message,
                    }
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

    @app.route("/api/dashboard", methods=["GET"])
    @jwt_required()  # new line
    def my_profile():
        try:
            # Call get_jwt_identity() to fetch userid for the logged-in user
            userid = get_jwt_identity()
            print("userid: " + str(userid))
            from .datalayer.event import EventDataLayer

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
            events = event_data.search_filter_sort(
                keyword=query,
                tag_name=tagname,
                location=location,
                club=club,
                start_time=start_time,
                end_time=end_time,
                sort_by=sortby,
            )
            print("returning event")
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

    @app.route("/api/favourites", methods=["GET"])
    @jwt_required()  # new line
    def my_favourites():
        try:
            # Call get_jwt_identity() to fetch userid for the logged-in user
            userid = get_jwt_identity()
            print("userid: " + str(userid))
            from .datalayer.like import LikeDataLayer

            like_data = LikeDataLayer()
            favourite_events = like_data.get_liked_events(user_id=userid)

            return jsonify_event_list(favourite_events)

        except Exception as e:
            error_message = str(e)
            return (
                jsonify(
                    {
                        "error": "Failed to get favourite posts",
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

            from .datalayer.like import LikeDataLayer

            like_layer = LikeDataLayer()
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

            from .datalayer.like import LikeDataLayer

            like_layer = LikeDataLayer()
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
