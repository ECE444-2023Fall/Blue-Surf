from flask import jsonify, request


def setup_routes(app):
  @app.route("/api/autosuggest", methods=["GET"])
  def autosuggest():
      query = request.args.get("query")
      print('query: ', query)
      try:
        from datalayer_event import EventDataLayer
        event_data = EventDataLayer()
        results = event_data.get_search_results_by_keyword(query)
        suggestions = [event.title for event in results]
        for event in results:
            print(event.title)
        return jsonify(suggestions)
      except Exception as e:
          error_message = str(e)
          return jsonify({"error": "Failed to look and display post title", "error_message":error_message}), 500
    

  @app.route("/api/search", methods=["GET"])
  def search():
      query = request.args.get("query")
      print("Printing query: ", query)
      try:
        from datalayer_event import EventDataLayer
        event_data = EventDataLayer()
        results = event_data.get_search_results_by_keyword(query)
        json_event = [
            {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'location': event.location,
                'start_time': event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                'end_time': event.end_time.strftime("%Y-%m-%d %H:%M:%S"), 
            } for event in results
        ]
        return jsonify(json_event)
      except Exception as e:
          error_message = str(e)
          return jsonify({"error": "Failed to look for post", "error_message":error_message}), 500

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
        event_data = EventDataLayer()
        events = event_data.get_all_events()

        json_events = []

        for event in events:
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
        event_data = EventDataLayer()
        event = event_data.get_event_by_id(event_id)

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
        }

        return jsonify(json_event)
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": "Failed to get event", "error message": error_message}), 500
        
