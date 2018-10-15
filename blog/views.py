from flask import Blueprint, session, render_template

from application import db
from blog.models import Post, Category
from blog.forms import PostForm
from author.models import Author

blog_app = Blueprint('blog_app', __name__)

@blog_app.route('/')
def index():
    return render_template('blog/index.html')

@blog_app.route('/post', methods=('GET', 'POST'))
def post():
    form = PostForm()

    return render_template('blog/post.html',
        form=form
    )