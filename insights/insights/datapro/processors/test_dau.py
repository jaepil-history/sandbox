#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from insights.datapro import settings

from pymongo import MongoClient
from insights.datapro.api.dbhandler import DBHandler
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
        print 'calculating dau ...'
        counts = 0
        elapsed = 0
        last_doc_id = None
        start_cal = time.time()

        dau = models.DAUDistribution()

        for doc in db_handler.find_dau(app_id, start, end):
            counts += 1
            last_doc_id = doc['_id']
            dau.accumulate(doc)

        print 'last_doc_id = ' + str(last_doc_id)

        end_cal = time.time()
        elapsed = (end_cal - start_cal) * 1000
        print 'time to write db: ' + str(elapsed) + 'msec'
        print 'counted items: ' + str(counts)

        dau.counts = counts
        dau.last_doc_id = last_doc_id
        dau.runtime = elapsed

        print dau.__dict__
        dau.save(db_handler, app_id)


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