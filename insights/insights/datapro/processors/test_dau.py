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
        print 'calculating dau ...'
        counts = 0
        last_doc_id = None
        start_cal = datetime.utcnow()

        ret_end = datetime.combine(start_cal.date(), time())
        ret_start = start_cal.date() - timedelta(days=models.MAX_RETENTION_DAYS)
        ret_start = datetime.combine(ret_start, time())

        ret_array = []
        query = {'_dt': {'$gte':ret_start, '$lt':ret_end}}
        for ret in db_handler.find_from_processed(app_id, 'ret', query):
            # print ret
            # print (start_cal.date() - ret['_dt'].date()).days
            temp = {str((start_cal.date() - ret['_dt'].date()).days) : ret['nu']}
            ret_array.append(temp)

        # print 'ret_array' + str(ret_array)

        for i in range(models.MAX_RETENTION_DAYS):
            pass

        dau = models.DAUDistribution()
        query = {'l_in': {'$gte':start, '$lt':end}}
        for usr in db_handler.find_from_insights(app_id, 'usr', query):
            counts += 1
            last_doc_id = usr['_id']
            diff = (start_cal.date() - usr['c'].date()).days
            dau.accumulate(usr)
            # if today - usr['c'] > 0:
            #     pass

        # print 'last_doc_id = ' + str(last_doc_id)

        end_cal = datetime.utcnow()
        elapsed = (end_cal - start_cal).microseconds * 0.001
        print 'time to write db: ' + str(elapsed) + 'msec'
        # print 'counted items: ' + str(counts)

        dau.counts = counts
        dau.last_doc_id = last_doc_id
        dau.runtime = elapsed

        # print dau.to_python()
        query = {"t": dau.title}
        dau.upsert(db_handler, app_id, query)


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
    start = datetime.combine(yesterday, time())
    end = datetime.combine(today, time())

    run(db_handler, start, end)