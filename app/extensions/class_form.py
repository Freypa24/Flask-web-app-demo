from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, HiddenField, EmailField, SubmitField
from wtforms.validators import InputRequired, Length, Email, DataRequired


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


class RemoveEmployeeForm(FlaskForm):
    employee_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("Remove")


class AddEmployeeForm(FlaskForm):
    employee_id = SelectField("Select Employee", validators=[DataRequired()], coerce=int)
    submit = SubmitField("Add Employee")