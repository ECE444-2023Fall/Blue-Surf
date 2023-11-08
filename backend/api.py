from flask import jsonify, request
# from datalayer_event import EventDataLayer

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

def setup_routes(app):
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

          from datalayer_event import EventDataLayer
          event_data = EventDataLayer()
          event_data.update_event(event_id=post_id, title=updated_post["title"], description=updated_post["description"], 
                                  extended_description=updated_post["extended_description"],location=updated_post["location"])

          return jsonify({"message": "Post updated successfully"})
      except Exception as e:
          error_message = str(e)
          return jsonify({"error": "Failed to update post", "error message":error_message}), 500
    
  @app.route("/api/", methods=["GET"])
  def index():
    try:
        from datalayer_event import EventDataLayer
        from datalayer_tag import TagDataLayer
        event_data = EventDataLayer()
        tag_data = TagDataLayer()
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
                "start_time": event.start_time.strftime("%Y-%m-%d %H:%M:%S"),  # Convert to string
                "end_time": event.end_time.strftime("%Y-%m-%d %H:%M:%S"),  # Convert to string
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
        return jsonify({"error": "Failed to get all events", "error message": error_message}), 500

  @app.route("/api/<int:event_id>", methods=["GET"])
  def get_event(event_id):
    try:
        from datalayer_event import EventDataLayer
        from datalayer_tag import TagDataLayer
        event_data = EventDataLayer()
        event = event_data.get_event_by_id(event_id)

        tag_data = TagDataLayer()
        # tag_names = []
        # for tag in event.tags:
        #     tag_names.append(tag_data.get_tag_names_by_ids(tag))
            
        tags = event_data.get_tags_for_event(event_id=event.id)
        tag_names = [tag.name for tag in tags]
        
        # tag_names = tag_data.get_tag_names_by_ids(event_tag_ids)

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
        return jsonify({"error": "Failed to get event", "error message": error_message}), 500
        
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
    "like_count": 25
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