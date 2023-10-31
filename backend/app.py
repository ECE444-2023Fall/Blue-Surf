from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from mock_data.mock_events import mockEvents

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "NEED TO CHANGE"

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

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def signup():
    return render_template("register.html")
