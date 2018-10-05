from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from werkzeug.security import check_password_hash

from author.models import Author

class LoginForm(FlaskForm):
    email = EmailField('Email address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        author = Author.query.filter_by(
            email=self.email.data,
            ).first()

        if author:
            if not check_password_hash(author.password, self.password.data):
                self.password.errors.append('Incorrect email or password')
                return False
            return True
        else:
            self.password.errors.append('Incorrect email or password')
            return False

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', [validators.InputRequired()])
    email = EmailField('Email address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password', [
            validators.EqualTo('password', message='Passwords must match'),
    ])

    def validate_email(self, email):
        author = Author.query.filter_by(email=email.data).first()
        if author is not None:
            raise ValidationError('Email already in use, please use a different one.')
