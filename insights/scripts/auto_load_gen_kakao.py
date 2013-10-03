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

import datetime
import time
import logging

# Configure logging
# LOGFILE = '/usr/local/insights/autogen.log'
# logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)
# logger = logging.getLogger('autogen')

import settings


options = settings.parse_options()

class InsightsClient(object):
    #INSIGHTS_API_URL = "http://api.insights.appspand.com:8001/api/v1/"
    # INSIGHTS_API_URL = "http://192.168.0.170:8001/api/v1/"
    INSIGHTS_API_URL = "http://localhost:8001/api/v1/"

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
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100),
            'c': datetime.datetime.utcnow()
        }

        url = self.make_request(self.app_id, "apa", params)
        self.send_request(url)

    def track_apr(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100)
        }

        url = self.make_request(self.app_id, "apr", params)
        self.send_request(url)

    def track_cpu(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100)
        }

        url = self.make_request(self.app_id, "cpu", params)
        self.send_request(url)

    def track_lgt(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100)
        }

        url = self.make_request(self.app_id, "lgt", params)
        self.send_request(url)

    def track_wid(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100)
        }

        url = self.make_request(self.app_id, "wid", params)
        self.send_request(url)

    def track_evt(self):
        pass

    def track_ins(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100)
        }

        url = self.make_request(self.app_id, "ins", params)
        self.send_request(url)

    def track_inr(self):
        pass

    def track_msr(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100)
        }

        url = self.make_request(self.app_id, "msr", params)
        self.send_request(url)

    def track_its(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100),
            "iid": random.randint(1, 30)
        }

        url = self.make_request(self.app_id, "its", params)
        self.send_request(url)

    def track_itr(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100),
            "iid": random.randint(1, 30)
        }

        url = self.make_request(self.app_id, "itr", params)
        self.send_request(url)

    def track_gci(self):
        pass

    def track_mtu(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100),
            "iid": random.randint(1, 30),
            # cu 0 : USD, 1 : KWN, 2 : YEN ...etc
            "cu": random.randint(0, 1),
            "v": random.randint(100, 50000)
        }

        url = self.make_request(self.app_id, "mtu", params)
        self.send_request(url)

    def track_icu(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100),
            "iid": random.randint(1, 30)
        }

        url = self.make_request(self.app_id, "icu", params)
        self.send_request(url)

    def track_igr(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100),
            "data": random.randint(1, 30)
        }

        url = self.make_request(self.app_id, "igr", params)
        self.send_request(url)

    def track_pgr(self, uuid):
        params = {
            "uuid": uuid,
            "f": random.randint(0, 1000),
            "ul": random.randint(1, 100)
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
        # logger.warning('No registered application found')
        print 'No registered application found'
        return
    else :
        return apps



def main(options):
    # db_client_processed = MongoClient(host=options.mongodb_processed_connection_uri,
    #                             max_pool_size=options.mongodb_max_concurrent)
    # db_processed = db_client_processed[options.mongodb_processed_db_name]

    db_client_insights = MongoClient(host=options.mongodb_insights_connection_uri,
                                max_pool_size=options.mongodb_max_concurrent)
    db_insights = db_client_insights[options.mongodb_insights_db_name]

    apps = getApps(options)
    print apps

    # execute once initially
    http_clients = []
    for app in apps:
        http_clients.append(InsightsClient(app_id=str(app['_id'])))
        for uuid in range(23000, 30000):
            http_client = http_clients[apps.index(app)]
            # client actions
            http_client.track_apa(uuid)

    # for uuid in range(10000, 20000):
    #     # client and user are picked randomly
    #     http_client = http_clients[random.randint(0, len(apps) - 1)]
    #     # client actions
    #     time.sleep(0.5 * random.random())
    #     http_client.track_cpu(uuid)
    #     http_client.track_pgr(uuid)
    #     http_client.track_mtu(uuid)

    # repeat for statement everyday
    # http_clients = []
    # for app in apps:
    #     http_clients.append(InsightsClient(app_id=str(app['_id'])))

    for i in range(15000):
        # client and user are picked randomly
        http_client = http_clients[random.randint(0, len(apps) - 1)]
        uuid = random.randint(1000, 30000)
        # client actions
        http_client.track_cpu(uuid)
        http_client.track_lgt(uuid)
        http_client.track_wid(uuid)
        http_client.track_ins(uuid)
        http_client.track_msr(uuid)
        http_client.track_its(uuid)
        http_client.track_itr(uuid)
        http_client.track_mtu(uuid)
        http_client.track_icu(uuid)
        http_client.track_igr(uuid)


if __name__ == "__main__":
    main(options)
