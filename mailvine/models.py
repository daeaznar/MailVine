from datetime import datetime
from mailvine import db, login_manager
from flask_login import UserMixin


# loads logged iin user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # inherit UserMixin class
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


# Many to many relationship List-Contact
contacts = db.Table('contacts',
                    db.Column('list_id', db.Integer, db.ForeignKey('list.id'), primary_key=True),
                    db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True)
                    )


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


# Many to many relationship Contact-Mail
mails = db.Table('mails',
                 db.Column('contact_id', db.Integer, db.ForeignKey('contact.id'), primary_key=True),
                 db.Column('mail_id', db.Integer, db.ForeignKey('mail.id'), primary_key=True)
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
                            # Relationship with Mail class, secondary with mails table
                            backref=db.backref('recipients', lazy=True))

    def __repr__(self):
        return f"Contact('{self.name}', '{self.email}')"


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120), nullable=False, default='Check this out!')
    email_text = db.Column(db.Text, nullable=False)
    email_photo = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, nullable=False, default=1)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Many to one relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Many to many relationship Contact-Mail exists

    def __repr__(self):
        return f"Mail('{self.subject}', '{self.sent_at}')"
