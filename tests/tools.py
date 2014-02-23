"""
Tools to help test StudyGroup.
"""

import os
import unittest
import tempfile

from flask.ext.testing import TestCase

from studygroup.application import create_app, db


class StudyGroupTestCase(TestCase):
    """
    Base class for all StudyGroup tests.
    """
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        # Use an in-memory SQLite db.
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
