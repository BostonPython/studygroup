import os
get = os.environ.get


MEETUP_GROUP_ID = get('MEETUP_GROUP_ID')
MEETUP_OAUTH_KEY = get('MEETUP_OAUTH_KEY')
MEETUP_OAUTH_SECRET = get('MEETUP_OAUTH_SECRET')

SQLALCHEMY_DATABASE_URI = 'postgresql://freedom@localhost/studygroup'

DEFAULT_MAX_MEMBERS = 10


# import local config to override global config
try:
    from settings_local import *
except ImportError:
    pass