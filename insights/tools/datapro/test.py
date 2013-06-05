#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

__author__ = 'byouloh'

import sys

sys.path.append("/GIT/appspand/insights")
# for i in sys.path:
#     print i
from pymongo import MongoClient

import tornado.options

import settings
from insights.api import models


options = settings.parse_options()
options.define(name="list", type=bool, default=False, help="List all applications")


def open_db_clients(connection_uri, db_name):
    db_client = MongoClient(host=connection_uri)
    db = db_client[db_name]
    return db


def test_open_db_clients(connection_uri, db_name, appId):
    db_client = MongoClient(host=connection_uri)
    db = db_client[db_name]

    col_all_name = appId + '.event.all'
    col_cpu_name = appId + '.event.cpu'
    col_all = db[col_all_name]
    col_cpu = db[col_cpu_name]

    print list(col_all.find().limit(5))
    print list(col_cpu.find().limit(5))


def list_application(config):
    db_client = MongoClient(host=config.mongodb_appspand_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_application = db_appspand.application

    return list(col_application.find())


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


def main(options):
    list = list_application(options)
    print list

    insights_config = []

    for app in list:
        temp = {}
        temp['app_id'] = str(app['_id'])
        temp['cluster_name'] = app['cluster']['name']
        temp['db_name'] = app['cluster']['db_name']
        temp['app_name'] = app['name']
        temp['db'] = open_db_clients("mongodb://localhost:27017", app['cluster']['db_name'])
        insights_config.append(temp)
        print insights_config







# def main(args):
#     if len(args) < 2:
#         print "load_gen.py [App ID]"
#         return
#
#     app_id = args[1]
#
#     client = InsightsClient(app_id=app_id)
#
#     for uuid in range(10000, 12000):
#         client.track_apa(uuid)
#         client.track_pgr(uuid)
#         client.track_cpu(uuid)
#         client.track_pgr(uuid)
#         #client.track_mtu(uuid)


if __name__ == "__main__":
    main(options)