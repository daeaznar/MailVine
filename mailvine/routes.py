import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from mailvine import app, db, bcrypt
from mailvine.forms import RegistrationForm, LoginForm, UpdateAccountForm
from mailvine.models import User, List, Contact, Mail
from flask_login import login_user, current_user, logout_user, login_required


# Index
@app.route('/')
def index():
    return render_template('index.html')


# User Registration/Sign up
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # hashes password
        user = User(first_name=form.firstName.data, last_name=form.lastName.data, email=form.email.data,
                    password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created. Welcome to MailVine {form.firstName.data}!", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()  # checks or valid user
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)  # logs in user with a session
                # gets next page to redirect when no user is logged and route is set manually from the browser to a
                # logged in only route
                next_page = request.args.get('next')
                # redirects to next_page if rout input is manual, otherwise renders dashboard
                return redirect(next_page) if next_page else render_template('dashboard.html')
            else:
                flash("Incorrect Email or Password. Login unsuccessful", 'danger')
        return render_template('login.html', form=form)


# log out user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# User dashboard when logged in
@app.route('/dashboard.html')
def dashboard():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('index'))


# function for new profile pictures. Saves img in directory, changes name keeping original extension
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_pics', picture_fn)
    output_size = (300, 300)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    
    img.save(picture_path)
    return picture_fn


# User Account info
@app.route("/account", methods=['GET', 'POST'])
@login_required  # user has to be logged in to access accounts
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.first_name = form.firstName.data
        current_user.last_name = form.lastName.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.firstName.data = current_user.first_name
        form.lastName.data = current_user.last_name
        form.email.data = current_user.email
    img_file = url_for('static', filename='img/profile_pics/' + current_user.img_file)
    return render_template('account.html', img_file=img_file, form=form)
