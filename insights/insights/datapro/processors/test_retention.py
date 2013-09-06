#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from insights.datapro import settings

from pymongo import MongoClient
from insights.datapro.api.dbhandler_pymongo import DBHandler
from datetime import datetime, timedelta
from insights.datapro.api import models
import time

def init_database(config):
    mongodb_client = MongoClient(host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size)

    return mongodb_client

def run(db_handler, start, end):
    app_ids = db_handler.get_app_ids_from_appspand()

    for app_id in app_ids:
        counts = 0
        elapsed = 0
        last_doc_id = None
        start_cal = time.time()

        for doc in db_handler.find_from_insights(app_id, 'apa', start, end):
            counts += 1
            last_doc_id = doc['_id']
            user = models.User()
            user.created_at = doc['nru']
            user.friends_count = doc['f']
            user.user_uid = doc['uuid']
            user.user_level = doc['ul']
            user.save(db_handler, app_id, 'usr', validate=True)

        print 'last_doc_id = ' + str(last_doc_id)

        end_cal = time.time()
        elapsed = (end_cal - start_cal) * 1000
        print 'time to write db: ' + str(elapsed) + 'msec'
        print 'counted items: ' + str(counts)


if __name__ == "__main__":
    config = settings.parse_options()
    db_client = init_database(config=config)
    dbs = {
        "appspand": db_client,
        "insights": db_client,
        "processed": db_client,
        "config": config
    }

    db_handler = DBHandler(dbs)

    today = datetime.utcnow().date() + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    start = datetime(yesterday.year, yesterday.month, yesterday.day, 00, 00, 00)
    end = datetime(today.year, today.month, today.day, 00, 00, 00)

    run(db_handler, start, end)