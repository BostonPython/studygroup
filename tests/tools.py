"""
Tools to help test StudyGroup.
"""

import os.path

import flask.ext.migrate
from flask.ext.testing import TestCase

from studygroup.application import create_app, db, create_baseline_data
from studygroup.models import User


DB_PATH = 'sqlite:///' + os.path.dirname(__file__) + '/../test.db'


class StudyGroupTestCase(TestCase):
    """
    Base class for all StudyGroup tests.
    """
    def setUp(self):
        flask.ext.migrate.upgrade()
        self.alice_id = self.create_user(full_name='Alice B.')
        self.admin_id = self.create_user(full_name='Bob Admin', is_admin=True)

    def tearDown(self):
        db.session.execute('DROP TABLE alembic_version')
        db.session.remove()
        db.drop_all()

    def create_app(self):
        """
        Method required by Flask-Testing to create the app object.
        """
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        # Use a SQLite db. Migrations will not work on an in-memory db.
        app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
        app.config['SQLALCHEMY_POOL_SIZE'] = None
        return app

    def create_user(self, **kwargs):
        """
        Make a new user, and return the user id.
        """
        user = User(**kwargs)
        import sqlalchemy.schema
        metadata = sqlalchemy.schema.MetaData()
        metadata.reflect(db.session.bind)
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
