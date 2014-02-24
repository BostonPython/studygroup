"""
Tools to help test StudyGroup.
"""

import unittest

from flask import session
from flask.ext.testing import TestCase

from studygroup.application import create_app, db
from studygroup.models import User


class StudyGroupTestCase(TestCase):
    """
    Base class for all StudyGroup tests.
    """
    def setUp(self):
        db.create_all()
        self.alice_id = self.create_user(full_name="Alice B. Admin")

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        """
        Method required by Flask-Testing to create the app object.
        """
        app = create_app()
        app.config['TESTING'] = True
        # Use an in-memory SQLite db.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        return app

    def create_user(self, **kwargs):
        """
        Make a new user, and return the user id.
        """
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user.id

    def login(self, user_id):
        """
        Log in a user by user id.
        """
        with self.client.session_transaction() as session:
            session['user_id'] = user_id
