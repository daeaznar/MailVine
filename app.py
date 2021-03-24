from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Login
@app.route('/login.html')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(port=3000, debug=True)

