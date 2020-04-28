from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://cjzalftyeobeti:8bdef532d3b7e3e2bc817ad874116bb878f192e0e20ab43bc85f9bbbedebeb05@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d1u5irucd38qh1')
db = scoped_session(sessionmaker(bind=engine))


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = db.execute("SELECT * from users where username = :username", {"username": username.data}).fetchone()
        if user:
            raise ValidationError('This username is taken. Please choose another')

    def validate_email(self, email):
        user = db.execute("SELECT * from users where email = :email", {"email": email.data}).fetchone()
        if user:
            raise ValidationError('This username is taken. Please choose another')

class LoginForm(FlaskForm):
    username1 = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    submit_login = SubmitField('Sign In')
