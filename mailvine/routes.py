from flask import render_template, flash, redirect, url_for
from mailvine import app
from mailvine.forms import RegistrationForm, LoginForm
from mailvine.models import User, List, Contact, Mail


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
