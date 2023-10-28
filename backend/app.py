from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'NEED TO CHANGE'


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def signup():
    return render_template('register.html')

@app.route('/postcreation', methods=['GET', 'POST'])
def postcreation():
    return render_template('postcreation.html')