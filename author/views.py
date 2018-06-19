from flask import Blueprint

author_app = Blueprint('author_app', __name__)

@author_app.route('/register', methods=('GET', 'POST'))
def register():
    return 'Author Registration'
