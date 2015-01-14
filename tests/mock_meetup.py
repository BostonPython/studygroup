from functools import wraps
import json
from collections import namedtuple
from flask import redirect

Response = namedtuple('Response', ['data', 'status'])


class MockMeetup(object):

    def get(self, *args, **kwargs):
        return Response(data=json.dumps({'id': 20, name:'steve'}))

    def post(self, *args, **kwargs):
        return None

    def authorized_handler(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated

    def authorize(self, callback=None, state=None):
        if callback is not None:
            return redirect(callback)

        return None

    def tokengetter(self, *args, **kwargs):
        return None


def remote_app(name, register=True, **kwargs):
    return MockMeetup()


def init_app(app):
    pass