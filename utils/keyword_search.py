from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
DATA = ["apple", "banana", "cherry", "date", "grape", "kiwi"]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    suggestions = [item for item in DATA if query in item]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
