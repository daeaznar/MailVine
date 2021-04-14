from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import RegistrationForm, LoginForm

# from flask_mysqldb import MySQL

app = Flask(__name__)

# Secret Key to protect data. Protection against cookie data tampering.
app.config['SECRET_KEY'] = '2a44893ff4337692349481e9a9e77e75'

# region DataBase structure

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mailvine.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    # One to many relationship with List
    lists = db.relationship('List', backref='user', lazy=True)
    # One to many relationship with Mail
    mails = db.relationship('Mail', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name} {self.last_name}', '{self.email}', '{self.img_file}')"


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Many to one relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Many to many relationship List-Contact
    contacts = db.relationship('Contact', secondary=contacts, lazy='subquery',
                               backref=db.backref('lists', lazy=True))

    def __repr__(self):
        return f"List('{self.name}', '{self.description}')"


# Many to many relationship List-Contact
contacts = db.Table('contacts',
                    db.Column('list_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
                    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True)
                    )


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, nullable=False, default=1)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Many to many relationship List-Contact exists
    # Many to many relationship Contact-Mail
    mails = db.relationship('Mail', secondary=mails, lazy='subquery',
                            backref=db.backref('contacts', lazy=True))

    def __repr__(self):
        return f"Contact('{self.name}', '{self.email}')"


# Many to many relationship Contact-Mail
mails = db.Table('mails',
                 db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True),
                 db.Column('mail_id', db.Integer, db.ForeignKey('mail.id'), primary_key=True)
                 )


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_text = db.Column(db.Text, nullable=False)
    email_photo = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, nullable=False, default=1)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Many to one relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Many to many relationship Contact-Mail exists

    def __repr__(self):
        return f"Contact('{self.name}', '{self.email}')"

# endregion


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
