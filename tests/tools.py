"""
Tools to help test StudyGroup.
"""
from flask.ext.testing import TestCase
import mock

from studygroup.application import create_app, db
from studygroup.models import User


class StudyGroupTestCase(TestCase):
    """
    Base class for all StudyGroup tests.
    """
    def setUp(self):
        # If a test needs to send messages the class must define send_messages True
        # Otherwise no test should send messages.
        if not getattr(self, 'send_messages', False):
            self.patcher = mock.patch('studygroup.messaging.meetup.post', spec=True)
            self.patcher.start()

        db.create_all()
        self.alice_id = self.create_user(full_name="Alice B. Admin")

    def tearDown(self):
        if getattr(self, 'send_messages', False):
            self.patcher.stop()

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

    def assert302(self, response):
        self.assertStatus(response, 302)
