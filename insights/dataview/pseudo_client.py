import random
import sys

import tornado.httpclient
import tornado.httputil
import tornado.options

from pymongo import MongoClient

import time
import logging

# Configure logging
LOGFILE = '/usr/local/insights/autogen.log'
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)
logger = logging.getLogger('autogen')

import settings

options = settings.parse_options()

# db_client_processed = MongoClient(host=options.mongodb_processed_connection_uri,
#                             max_pool_size=options.mongodb_max_concurrent)
# db_processed = db_client_processed[options.mongodb_processed_db_name]

# db_client_appspand = MongoClient(host=options.mongodb_appspand_connection_uri,
#                             max_pool_size=options.mongodb_max_concurrent)
# db_appspand = db_client_appspand[options.mongodb_appspand_db_name]
# col_application = db_appspand.application
# print apps


class InsightsClient(object):
    INSIGHTS_API_URL = "http://api.insights.appspand.com:8001/api/v1/"

    def __init__(self, app_id):
        self.app_id = app_id

    def make_request(self, app_id, message_type, params):
        url = self.INSIGHTS_API_URL
        url += app_id + "/" + message_type + "/?"
        url += tornado.httputil.urlencode(params)

        return url

    def send_request(self, url):
        client = tornado.httpclient.HTTPClient()
        try:
            client.fetch(url)
        except tornado.httpclient.HTTPError as e:
            print "Error:", e
        client.close()

    def track_apa(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "apa", params)
        self.send_request(url)
