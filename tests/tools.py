"""
Tools to help test StudyGroup.
"""

from flask.ext.testing import TestCase

from studygroup.application import create_app, db, create_baseline_data
from studygroup.models import User


class StudyGroupTestCase(TestCase):
    """
    Base class for all StudyGroup tests.
    """
    def setUp(self):
        db.create_all()
        create_baseline_data()
        self.alice_id = self.create_user(full_name='Alice B.')
        self.admin_id = self.create_user(full_name='Bob Admin', is_admin=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        """
        Method required by Flask-Testing to create the app object.
        """
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
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
