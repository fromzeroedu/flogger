from flask import Blueprint, render_template, session

from application import db

blog_app = Blueprint('blog_app', __name__)

@blog_app.route('/')
def index():
    return render_template('blog/index.html')
