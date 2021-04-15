import os   # get file name and file extension
import secrets  #generate hex code for images
from PIL import Image   #manage photos, resize, save
from flask import render_template, flash, redirect, url_for, request, abort
from mailvine import app, db, bcrypt
from mailvine.forms import RegistrationForm, LoginForm, UpdateAccountForm, MailForm
from mailvine.models import User, List, Contact, Mail
from sqlalchemy.sql import  select
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
                # redirects to next_page if route input is manual, otherwise renders dashboard
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
#user has to be logged in to access, otherwise redirects to login. If redirected, aget login goes to requested route
@login_required    
def dashboard():
    #   select from Mail where user_id = current user
    user = User.query.get(current_user.id)
    mails = Mail.query.filter(Mail.user==user)
    return render_template('dashboard.html', mails=mails)



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
    elif request.method == 'GET':   # gets values that are already saved
        form.firstName.data = current_user.first_name
        form.lastName.data = current_user.last_name
        form.email.data = current_user.email
    img_file = url_for('static', filename='img/profile_pics/' + current_user.img_file)
    return render_template('account.html', img_file=img_file, form=form)


# function for mail attached photos. Saves img in directory, changes name keeping original extension
def attach_img(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/img/attached_img', picture_fn)
    output_size = (300, 300)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    
    img.save(picture_path)
    return picture_fn


# Create Mail
@app.route('/mail/new', methods=['GET', 'POST'])
@login_required  # user has to be logged in to access accounts 
def new_mail():
    form = MailForm()
    if form.validate_on_submit():
        if form.picture.data:
            img = attach_img(form.picture.data)
            mail = Mail(title=form.title.data, subject=form.subject.data, email_text=form.email_text.data, email_photo=img, user=current_user)
        else:
            mail = Mail(title=form.title.data, subject=form.subject.data, email_text=form.email_text.data, user=current_user)
        db.session.add(mail)
        db.session.commit()
        flash('Mail has been created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_mail.html', form=form, legend='New Mail')


@app.route('/mail/<int:mail_id>')
def mail(mail_id):
    mail = Mail.query.get_or_404(mail_id)
    return render_template('mail.html', mail=mail)



@app.route('/mail/<int:mail_id>/update', methods=['GET', 'POST'])
@login_required
def update_mail(mail_id):
    mail = Mail.query.get_or_404(mail_id)
    if mail.user != current_user:
        abort(403)
    form = MailForm()
    if form.validate_on_submit():
        mail.title = form.title.data
        mail.subject = form.subject.data
        mail.email_text = form.email_text.data
        mail.email_photo = form.picture.data
        db.session.commit()
        flash('Mail has been updated!', 'success')
        return redirect(url_for('mail', mail_id=mail.id))
    elif request.method == 'GET':
        form.title.data = mail.title
        form.subject.data = mail.subject
        form.email_text.data = mail.email_text
        form.picture.data = mail.email_photo
    return render_template('create_mail.html', form=form, legend='Update Mail')
