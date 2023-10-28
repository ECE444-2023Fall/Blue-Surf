from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "NEED TO CHANGE"


def autosuggest_from_database(query):
    mockSuggestions = [
        "Apple",
        "Banana",
        "Orange",
        "Strawberry",
        "Blueberry",
        "Mango",
        "Pineapple",
        "Watermelon",
        "Grapes",
        "Kiwi",
    ]

    query_length = len(query)
    if query_length == 0:
        matchedSuggestions = []
    else:
        matchedSuggestions = [suggestion for suggestion in mockSuggestions if suggestion.lower()[:query_length] == query.lower()]
    return matchedSuggestions


@app.route("/autosuggest", methods=["GET"])
def autosuggest():
    query = request.args.get("query")
    results = autosuggest_from_database(query)
    return jsonify(results)


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def signup():
    return render_template("register.html")
