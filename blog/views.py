from flask import Blueprint, render_template, session

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
        image = request.files.get('image')
        filename = None

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data

        author = Author.query.filter_by(username=session['username']).first()
        title = form.title.data
        body = form.body.data
        post = Post(
            author=author,
            title=title,
            body=body,
            category=category,
            filename=filename
        )
        db.session.add(post)
        # do the slug
        db.session.commit()
        # return redirect(url_for('article', slug=slug))
    return render_template('blog/post.html', form=form, action="new")

@blog_app.route('/article/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)
