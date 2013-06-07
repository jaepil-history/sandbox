#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

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

    def track_apr(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "apr", params)
        self.send_request(url)

    def track_cpu(self, uuid):
        birthday = ["%04d" % random.randint(1900, 2000),
                    "%02d" % random.randint(1, 12),
                    "%02d" % random.randint(1, 28)]
        gender = ["m", "f", "u"]
        country = ["Seoul", "Busan", "Incheon", "Jeju", "Jeonju", "Daejeon", "Daegu", "Pohang", "Gyeongju",
                   "Jinju", "Ulsan", "Chuncheon", "Anyang", "Bucheon", "Cheongju", "Gumi", "Gunsan"]

        params = {
            "uuid": uuid,
            "b": "/".join(birthday),
            "g": gender[random.randint(0, 2)],
            "lc": country[random.randint(0, 16)],
            "f": random.randint(0, 1000)
        }

        url = self.make_request(self.app_id, "cpu", params)
        self.send_request(url)

    def track_evt(self):
        pass

    def track_ins(self):
        pass

    def track_inr(self):
        pass

    def track_gci(self):
        pass

    def track_mtu(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "mtu", params)
        self.send_request(url)

    def track_pgr(self, uuid):
        params = {
            "uuid": uuid
        }

        url = self.make_request(self.app_id, "pgr", params)
        self.send_request(url)

    def track_pst(self):
        pass

    def track_psr(self):
        pass

    def track_ucc(self):
        pass

    def track_nes(self):
        pass

    def track_nei(self):
        pass


def open_db_clients(connection_uri, db_name):
    db_client = MongoClient(host=connection_uri)
    db = db_client[db_name]
    return db


def getApps(config):
    db_client = MongoClient(host=config.mongodb_appspand_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_application = db_appspand.application

    apps = list(col_application.find())

    if len(apps) < 1:
        logger.warning('No registered application found')
        print 'No registered application found'
        return
    else :
        return apps



def main(options):
    apps = getApps(options)
    print apps

    clients = []
    for app in apps:
        clients.append(InsightsClient(app_id=str(app['_id'])))

    for uuid in range(12000, 20000):
        # client is picked randomly
        client = clients[random.randint(0, len(apps) - 1)]

        '''
        # client actions
        '''
        # Generate data at random time(unit: milisecond)
        time.sleep(random.randint(0, 1000) * 0.001)
        client.track_apa(uuid)
        # Generate data at random time(unit: milisecond)
        time.sleep(random.randint(0, 1000) * 0.001)
        client.track_cpu(uuid)
        # Generate data at random time(unit: milisecond)
        time.sleep(random.randint(0, 1000) * 0.001)
        client.track_pgr(uuid)
        # Generate data at random time(unit: milisecond)
        time.sleep(random.randint(0, 1000) * 0.001)
        client.track_pgr(uuid)
        #client.track_mtu(uuid)


if __name__ == "__main__":
    main(options)
