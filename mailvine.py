from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

# from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret Key to protect data. Protection against cookie data tampering.
app.config['SECRET_KEY'] = '2a44893ff4337692349481e9a9e77e75'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mailvine.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.firstName}', '{self.email}', '{self.img_file}')"


# Index
@app.route('/')
def index():
    return render_template('index.html')


# Login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@mailvine.com' and form.password.data == 'pass':
            flash(f"You're logged in. Welcome!", 'success')
            return redirect(url_for('index'))
        else:
            flash("Login unsuccessful", 'danger')
    return render_template('login.html', form=form)


# User Registration/Sign up
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created successfully. Welcome to MailVine {form.firstName.data}!", 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
