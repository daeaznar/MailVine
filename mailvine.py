from flask import Flask, render_template, request, redirect, url_for
from forms import RegistrationForm, LoginForm

# from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret Key to protect data. Protection against cookie data tampering.
app.config['SECRET_KEY'] = '2a44893ff4337692349481e9a9e77e75'


# Index
@app.route('/')
def index():
    return render_template('index.html')


# Login
@app.route('/login.html')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


# User Registration/Sign up
@app.route('/register.html')
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
