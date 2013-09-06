#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from insights.datapro import settings

from pymongo import MongoClient
from insights.datapro.api.dbhandler_pymongo import DBHandler
from datetime import datetime, timedelta
from insights.datapro.api.models import BaseResult
import time

# class NewUser

def init_database(config):
    mongodb_client = MongoClient(host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size)

    return mongodb_client

def run(db_handler):
    app_ids = db_handler.get_app_ids()

    print app_ids

    start = datetime.utcnow() - timedelta(hours=1000)
    end = datetime.utcnow()
    app_id = "520472e035b6e6185caf70dc"

    print app_id
    print start
    print end

    base_result = models.UserDistributionByMinutes()

    counts = 0
    elapsed = 0
    last_doc_id = None
    start_cal = time.time()

    for doc in db_handler.cursor(app_id, 'cpu', start, end):
        counts += 1
        last_doc_id = doc['_id']
        base_result.accumulate(doc)

    print 'last_doc_id = ' + str(last_doc_id)

    end_cal = time.time()
    elapsed = (end_cal - start_cal) * 1000
    print 'time to read db: ' + str(elapsed) + 'msec'
    print 'counted items: ' + str(counts)

    base_result.last_doc_id = last_doc_id
    base_result.title = 'user_distribution'
    base_result.runtime = elapsed
    base_result.timestamp = int(time.time())
    base_result.counts = counts

    print base_result.__dict__
    print base_result.to_python()


    '''
    compare handling all list with one by one
    '''
    base_result1 = models.BaseResult()

    print base_result1.__dict__

    counts = 0
    elapsed = 0
    last_doc_id = None
    start_cal = time.time()

    memory = db_handler.find_to_list(app_id, 'cpu', start, end)

    for doc in memory:
        counts += 1
        last_doc_id = doc['_id']
        base_result1.accumulate(doc)

    print 'last_doc_id = ' + str(last_doc_id)

    end_cal = time.time()
    elapsed = (end_cal - start_cal) * 1000
    print 'time to read db: ' + str(elapsed) + 'msec'
    print 'counted items: ' + str(counts)

    base_result1.last_doc_id = last_doc_id
    base_result1.title = 'user_distribution'
    base_result1.runtime = elapsed
    base_result1.timestamp = int(time.time())
    base_result1.counts = counts

    print base_result1.__dict__
    print base_result1.to_python()


if __name__ == "__main__":
    config = settings.parse_options()
    db_client = init_database(config=config)
    dbs = {
        "appspand": db_client,
        "insights": db_client,
        "processed": db_client,
        "retention": db_client,
        "config": config
    }

    db_handler = DBHandler(dbs)
    run(db_handler=db_handler)