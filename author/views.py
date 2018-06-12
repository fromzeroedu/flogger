from flask import Blueprint, render_template, redirect, session, request, url_for, flash
from author.forms import RegisterForm, LoginForm
from author.models import Author
from werkzeug.security import generate_password_hash, check_password_hash

from application import db
from author.models import Author

author_app = Blueprint('author_app', __name__)

@author_app.route('/')
def init():
    return "<h1>Author Home</h1>"

@author_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        # check_password_hash(hash, 'barfoo')
        author = Author(
            form.full_name.data,
            form.email.data,
            hashed_password
        )
        db.session.add(author)
        db.session.commit()
        return redirect('/success')
    return render_template('author/register.html', form=form)

@author_app.route('/success')
def success():
    return "Author registered!"
