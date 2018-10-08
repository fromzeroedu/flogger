from flask import Blueprint, render_template, redirect, session, request, url_for, flash
from werkzeug.security import generate_password_hash

from application import db
from author.models import Author
from author.forms import RegisterForm, LoginForm

author_app = Blueprint('author_app', __name__)

@author_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        author = Author(
            form.full_name.data,
            form.email.data,
            hashed_password
        )
        db.session.add(author)
        db.session.commit()
        flash("You are now registered, please login")
        return redirect(url_for('.login'))
    return render_template('author/register.html', form=form)

@author_app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(email=form.email.data).first()
        session['id'] = author.id
        session['full_name'] = author.full_name
        if 'next' in session:
            next = session.get('next')
            session.pop('next')
            return redirect(next)
        else:
            return redirect(url_for('blog_app.index'))

    return render_template('author/login.html', form=form, error=error)

@author_app.route('/logout')
def logout():
    session.pop('id')
    session.pop('full_name')
    flash("User logged out")
    return redirect(url_for('.login'))
