from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField

from author.models import Author

class LoginForm(FlaskForm):
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

class RegisterForm(LoginForm):
    full_name = StringField('Full Name', [validators.Required()])
    confirm = PasswordField('Repeat Password', [
            validators.EqualTo('password', message='Passwords must match'),
    ])

    def validate_email(self, email):
        author = Author.query.filter_by(email=email.data).first()
        if author is not None:
            raise ValidationError('Email already in use, please use a different one.')
