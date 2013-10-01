#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from insights.datapro import settings

from pymongo import MongoClient
from insights.datapro.api.dbhandler import DBHandler
from datetime import datetime, timedelta, time
from insights.datapro.api import models

def init_database(config):
    mongodb_client = MongoClient(host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size)

    return mongodb_client

def run(db_handler, start, end):
    app_ids = db_handler.get_app_ids_from_appspand()

    for app_id in app_ids:
        print 'calculating nru ...'
        counts = 0
        last_doc_id = None
        start_cal = datetime.utcnow()

        nru = models.NRUDistribution()
        ret = models.UserRetention()
        #ret.title

        middle = ["%04d" % start.year, "%02d" % start.month]
        middle_name = ".".join(middle)

        query = {'_dt': {'$gte':start, '$lt':end }}
        for doc in db_handler.find_from_insights(app_id, middle_name, 'apa', query):
            counts += 1
            last_doc_id = doc['_id']
            nru.accumulate(doc)

        ret.new_users = counts
        print ret.to_python()
        query = {"t": ret.title}
        ret.upsert(db_handler, app_id, query)

        # print 'last_doc_id = ' + str(last_doc_id)

        end_cal = datetime.utcnow()
        elapsed = (end_cal - start_cal).microseconds * 0.001
        print 'time to write db: ' + str(elapsed) + 'msec'
        # print 'counted items: ' + str(counts)

        nru.counts = counts
        nru.last_doc_id = last_doc_id
        nru.runtime = elapsed

        print nru.to_python()
        query = {"t": nru.title}
        nru.upsert(db_handler, app_id, query)
        # nru.save(db_handler, app_id)


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

    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    start = datetime.combine(yesterday, time())
    end = datetime.combine(today, time())

    run(db_handler, start, end)