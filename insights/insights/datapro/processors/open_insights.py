#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand


import sys

# sys.path.append("/GIT/appspand/insights")
# for i in sys.path:
#     print i
from pymongo import MongoClient
import settings


options = settings.parse_options()

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


def getApps(config):
    db_client = MongoClient(host=config.mongodb_appspand_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_application = db_appspand.application

    return list(col_application.find())

def main(options):
    db_client_processed = MongoClient(host=options.mongodb_processed_connection_uri,
                            max_pool_size=options.mongodb_max_concurrent)
    apps = getApps(options)
    print apps

    insights_config = []

    for app in apps:
        temp = {}
        temp['app_id'] = str(app['_id'])
        temp['cluster_name'] = app['cluster']['name']
        temp['db_name'] = app['cluster']['db_name']
        temp['app_name'] = app['name']
        temp['db'] = open_db_clients("mongodb://localhost:27017", app['cluster']['db_name'])
        insights_config.append(temp)

    print insights_config


if __name__ == "__main__":
    main(options)