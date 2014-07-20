from flask import Flask
from flask_oauthlib.client import OAuth
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

import settings


db = SQLAlchemy()
oauth = OAuth()


def create_app(debug=True):
    from views import studygroup

    app = Flask(__name__)
    app.debug = debug
    app.secret_key = 'development'
    app.config.from_object(settings)

    app.register_blueprint(studygroup)

    Bootstrap(app)
    db.init_app(app)
    oauth.init_app(app)

    return app


meetup = oauth.remote_app(
    'meetup',
    consumer_key=settings.MEETUP_OAUTH_KEY,
    consumer_secret=settings.MEETUP_OAUTH_SECRET,
    request_token_params={'scope': 'messaging'},
    base_url='https://api.meetup.com/',
    access_token_method='POST',
    access_token_url='https://secure.meetup.com/oauth2/access',
    authorize_url='https://secure.meetup.com/oauth2/authorize'
)
