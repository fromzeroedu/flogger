from flask import Blueprint, session, render_template
from slugify import slugify

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

    if form.validate_on_submit():
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data

        author = Author.query.get(session['id'])
        title = form.title.data.strip()
        body = form.body.data.strip()
        post = Post(
            author=author,
            title=title,
            body=body,
            category=category,
        )

        db.session.add(post)
        db.session.commit()

        slug = slugify(str(post.id) + '-' + post.title)
        post.slug = slug
        db.session.commit()

    return render_template('blog/post.html',
        form=form
    )