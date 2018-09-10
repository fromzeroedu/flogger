from flask import Blueprint, render_template

from author.models import Author
from author.forms import RegisterForm

author_app = Blueprint('author_app', __name__)

@author_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    return render_template('author/register.html', form=form)
