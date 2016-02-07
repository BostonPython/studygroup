import os
get = os.environ.get

MEETUP_GROUP_ID = get('MEETUP_GROUP_ID')
MEETUP_OAUTH_KEY = get('MEETUP_OAUTH_KEY')
MEETUP_OAUTH_SECRET = get('MEETUP_OAUTH_SECRET')
SQLALCHEMY_DATABASE_URI = get('SQLALCHEMY_DATABASE_URI')
DEFAULT_MAX_MEMBERS = 10

WEBPACK_MANIFEST_PATH = "/Users/mmilkin/code/studygroup/manifest.json"

# import local config to override global config
try:
    from settings_local import *
except ImportError:
    pass
