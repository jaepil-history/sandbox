#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

import settings

from pymongo import MongoClient
from api import models
from api.dbhandler import DBHandler
from datetime import datetime, timedelta, time

def init_database(config):
    mongodb_client = MongoClient(host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size)

    return mongodb_client

def cal_nru(db_handler, app_id, start, end):
    print 'calculating nru ...'
    counts = 0
    last_doc_id = None
    start_cal = datetime.utcnow()

    nru = models.NRUDistribution()
    ret = models.UserRetention()

    # fix it when 2 months needed
    middle = ["%04d" % start.year, "%02d" % start.month]
    middle_name = ".".join(middle)

    query = {'_dt': {'$gte':start, '$lt':end }}
    for doc in db_handler.find_from_insights(app_id, middle_name, 'apa', query):
        counts += 1
        last_doc_id = doc['_id']
        nru.accumulate(doc)

    ret.new_users = counts
    query = {"t": ret.title}
    ret.upsert(db_handler, app_id, query)

    end_cal = datetime.utcnow()
    elapsed = (end_cal - start_cal).microseconds * 0.001

    nru.counts = counts
    nru.last_doc_id = last_doc_id
    nru.runtime = elapsed

    query = {"t": nru.title}
    nru.upsert(db_handler, app_id, query)


def cal_dau_retention(db_handler, app_id, start, end):
    print 'calculating dau ...'
    counts = 0
    last_doc_id = None
    start_cal = datetime.utcnow()

    ret_end = end + timedelta(days=1)
    ret_start = end - timedelta(days=models.MAX_RETENTION_DAYS - 1)
    ret_start = datetime.combine(ret_start, time())

    print 'calculating retention ...'
    ret_array = [0 for _ in range(models.MAX_RETENTION_DAYS)]

    dau = models.DAUDistribution()
    query = {'l_in': {'$gte':start, '$lt':end}}
    for usr in db_handler.find_from_usr(app_id, query):
        counts += 1
        last_doc_id = usr['_id']
        diff = (start_cal.date() - usr['c'].date()).days - 1
        dau.accumulate(usr)
        ret_array[diff] += 1

    query = {'_dt': {'$gte':ret_start, '$lt':ret_end}}
    for ret in db_handler.find_from_processed(app_id, 'retention', query):
        diff = (start_cal.date() - ret['_dt'].date()).days
        if ret['nu'] != 0:
            ret_array[diff] = float(ret_array[diff]) / float(ret['nu'])
        else:
            ret_array[diff] = 0.0
        ret['ret'][diff] = ret_array[diff]
        db_handler.upsert_to_processed(app_id, 'retention', {"_id": ret['_id']}, ret)

    #query = {'_dt': {'$gte':ret_start, '$lt':ret_end}}
    #for ret in db_handler.find_from_processed(app_id, 'retention', query):
    #    print 'updated ret: ' + str(ret)

    end_cal = datetime.utcnow()
    elapsed = (end_cal - start_cal).microseconds * 0.001

    dau.counts = counts
    dau.last_doc_id = last_doc_id
    dau.runtime = elapsed

    query = {"t": dau.title}
    dau.upsert(db_handler, app_id, query)


def run(db_handler, start, end):
    app_ids = db_handler.get_app_ids_from_appspand()

    for app_id in app_ids:
        cal_nru(db_handler, app_id, start, end)
        cal_dau_retention(db_handler, app_id, start, end)


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
