from flask import Blueprint, render_template

from author.models import Author
from author.forms import RegisterForm

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
        return "Validated"
    return render_template('author/register.html', form=form)
