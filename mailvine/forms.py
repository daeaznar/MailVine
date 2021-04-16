from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import current_user
from mailvine.models import User


# Registration form
class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # validates if email is registered
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # first coincidence with that email
        if user:
            raise ValidationError('An account is already registered with that email')
    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')


# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


# update account info form
class UpdateAccountForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # validates if email is registered
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()  # first coincidence with that email
            if user:
                raise ValidationError('An account is already registered with that email')


class MailForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    email_text = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Attach Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')


class ListForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired()])
    description = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Save')


class SendMailForm(FlaskForm):
    email = StringField('Recipient Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')
