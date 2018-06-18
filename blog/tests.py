import os
import unittest
import pathlib
from flask import session
from slugify import slugify

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))

from author.models import Author
from application import db
from application import create_app as create_app_base
from utils.test_db import TestDB

class PostTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(
            SQLALCHEMY_DATABASE_URI=self.db_uri,
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY = 'mySecret!'
        )

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        with self.app_factory.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()
        self.test_db.drop_db()

    def user_dict(self):
        return dict(
            full_name='John Smith',
            email='jsmith@example.com',
            password='test123',
            confirm='test123'
        )

    def post_dict(self):
        return dict(
            title='My Awesome Post',
            body='This is my awesome post content',
            new_category='Tech',
            tags_field='flask, python'
        )

    def test_blog_post_create(self):
        # Post without logging in
        rv = self.app.get('/post', follow_redirects=True)
        assert 'Please login to continue' in str(rv.data)

        # Register and login
        rv = self.app.post('/register', data=self.user_dict())
        rv = self.app.post('/login', data=self.user_dict())

        # post first post
        rv = self.app.post('/post', data=self.post_dict(),
            follow_redirects=True)
        assert 'Article posted' in str(rv.data)
        assert 'Tech' in str(rv.data) # category
        assert 'flask' in str(rv.data) # tag

    def test_blog_post_update_delete(self):
        # Register and post
        rv = self.app.post('/register', data=self.user_dict())
        rv = self.app.post('/login', data=self.user_dict())
        rv = self.app.post('/post', data=self.post_dict())

        # edit the article
        post2 = self.post_dict()
        post2['title'] = 'My New Awesome Post'
        post2['tags_field'] = 'django'
        rv = self.app.post('edit/1-' + slugify(self.post_dict()['title']),
            data=post2,
            follow_redirects=True)
        assert 'Article edited' in str(rv.data)
        assert 'My New Awesome Post' in str(rv.data)
        assert 'flask' not in str(rv.data)

        # delete the article
        rv = self.app.get('/delete/1-' + slugify(post2['title']),
            follow_redirects=True)
        assert 'Article deleted' in str(rv.data)
