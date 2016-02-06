from functools import wraps
from flask import g, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if getattr(g, 'user', None) is None:
            return redirect(url_for('studygroup.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
