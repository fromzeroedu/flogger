from flask import Blueprint, session, render_template, flash, redirect, url_for
from slugify import slugify

from application import db
from blog.models import Post, Category
from blog.forms import PostForm
from author.models import Author
from author.decorators import login_required

blog_app = Blueprint('blog_app', __name__)

POSTS_PER_PAGE = 5

@blog_app.route('/')
def index():
    page = int(request.values.get('page', '1'))
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc())\
        .paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html',
        posts=posts
    )

@blog_app.route('/post', methods=('GET', 'POST'))
@login_required
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

        flash('Article posted')
        return redirect(url_for('.article', slug=slug))

    return render_template('blog/post.html',
        form=form
    )

@blog_app.route('/posts/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/article.html', post=post)