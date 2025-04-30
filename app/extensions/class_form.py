from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, Email


class SignupForm(FlaskForm):
    full_name = StringField('Full_name', validators=[InputRequired('Username required'),
                                                     Length(min=3, max=60, message="Username must be in 3 to 60 characters")])
    email = EmailField('Email', validators=[InputRequired('Email required'), Email()])
    password = PasswordField('Password', validators=[InputRequired('Password required')])
    confirm_password = PasswordField('Password', validators=[InputRequired('Please confirm your password')])
    submit = SubmitField('Submit')


class SigninForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired('Email required'), Email()])
    password = PasswordField('Password', validators=[InputRequired('Password required')])
    submit = SubmitField('Submit')
