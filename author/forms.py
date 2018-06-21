from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', [validators.DataRequired()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', [
            validators.DataRequired(),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password', [
            validators.EqualTo('password', message='Passwords must match'),
    ])
