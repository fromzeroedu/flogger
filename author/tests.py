import os
import unittest
import pathlib
from flask import session

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))

from author.models import Author
from application import db
from application import create_app as create_app_base
from utils.test_db import TestDB

class AuthorTest(unittest.TestCase):
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

    def test_user_register(self):
        # Check user registration
        rv = self.app.post('/register', data=self.user_dict(),
            follow_redirects=True)
        assert 'You are now registered' in str(rv.data)

        # If we want to check things as we were running in a views.py
        # we need to instantiate a context
        with self.app as c:
            rv = c.get('/')
            assert Author.query.filter_by(email=self.user_dict()['email']).count() == 1

        # Try to register user with the same email
        rv = self.app.post('/register', data=self.user_dict(),
            follow_redirects=True)
        assert 'Email already in use' in str(rv.data)

        # Try to register user with mismatching passwords
        user2 = self.user_dict()
        user2['email'] = 'john@example.com'
        user2['confirm'] = 'test456'
        rv = self.app.post('/register', data=user2,
            follow_redirects=True)
        assert 'Passwords must match' in str(rv.data)
