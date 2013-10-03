import sys
try:
    import json
except ImportError:
    import simplejson as json

from os.path import join, abspath, dirname

PROJECT_ROOT = abspath(dirname(__file__))
TEMPLATES_DIR = join(PROJECT_ROOT, 'templates')

config_path = 'config/dataview.conf'
try:
    config_file = file(config_path).read()
    config = json.loads(config_file)
except Exception, e:
    print "There was an error in your configuration file: " + config_path
    raise e

#  DataView Defaults
BACKEND = config.get('backend', 'mongodb')

_backend = config.get('backend', {})
_mongo = _backend.get('mongo', {})
_web_app = config.get('web_app', {})

MONGO = {
    'port': _mongo.get('port', 27017),
    'host': _mongo.get('host', '127.0.0.1'),
    'user': _mongo.get('user', ''),
    'password': _mongo.get('password', ''),
    'database' : 'processed',
}

PROCESSED_LIST = config.get('processed_list', [])
APP_ID = config.get('app_id', '5226e77335b6e61184d73e39')

host = _web_app.get('host', 'http://127.0.0.1')

if not host.startswith('http'):
    host = "http://{0}".format(host)

WEB_APP = {
    'host': host,
    'port': _web_app.get('port', 8888)
}

ACL = config.get('acl', "False") # Expects string
key = config.get('secret_key', None)
PROXY = config.get('proxy', None) # Relative baseurl if true
ZEROMQ = config.get('zeromq', '127.0.0.1:5464') # TCP address for the ZeroMQ daemon

TIMEZONE = config.get('timezone','UTC')

if key != None and len(key) > 0:
    SECRET_KEY = key
else:
    SECRET_KEY = 'TGJKhSSeZaPZr24W6GlByAaLVe0VKvg8qs+8O7y=' #Don't break the dataview

#DISCOVERY = config.get('discovery', [])
#EMAILS = config.get('emails', [])
#EVENTS = config.get('events', [])
#INSTALLS = config.get('installs', [])
#INVITES = config.get('invites', [])
#MESSAGES = config.get('messages', [])
#MONETIZATION = config.get('monetization', [])
#NOTIFICATIONS = config.get('notifications', [])
#VIRALITY = config.get('virality', [])
#RETURNING_USERS = config.get('returning_users', [])
#STREAM = config.get('stream', [])
#TRAFFIC = config.get('traffic', [])
#TIME = config.get('time', [])
#USER_DISTRIBUTION = config.get('user_distribution', [])
#USER_RETENTION = config.get('user_retention', [])
#USER_SESSIONS = config.get('user_sessions', [])
#UNIQUE_VISITORS = config.get('unique_visitors', [])