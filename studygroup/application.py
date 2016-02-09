from flask import Flask
from flask_oauthlib.client import OAuth
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

import settings


db = SQLAlchemy()
oauth = OAuth()
migrate = Migrate()


def create_app(debug=True):
    from views import studygroup
    from groups import groups
    app = Flask(__name__)
    app.debug = debug
    app.secret_key = 'development'
    app.config.from_object(settings)

    app.register_blueprint(studygroup)
    app.register_blueprint(groups)

    db.init_app(app)
    oauth.init_app(app)
    migrate.init_app(app, db)

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
