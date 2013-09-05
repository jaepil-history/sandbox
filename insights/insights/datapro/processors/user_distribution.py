#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from insights.datapro import settings

from pymongo import MongoClient
from insights.datapro.api.dbhandler_pymongo import DBHandler

def init_database(config):
    mongodb_client = MongoClient(host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size)

    return mongodb_client

def run(db_handler):
    app_ids = db_handler.get_app_ids()

    print app_ids

    from datetime import datetime, timedelta

    start = datetime.utcnow() - timedelta(hours=1000)
    end = datetime.utcnow()
    app_id = "520472e035b6e6185caf70dc"

    print app_id
    print start
    print end

    # for doc in db_handler.cursor(app_id, 'cpu', start, end):
    #     print doc

    print '==============================================================='

    # result = db_handler.find_to_list(app_id, 'apa', start, end)
    # print result
    #
    # print db_handler.get_column_values(app_id, 'apa', 'uuid', start, end)
    #
    # users = db_handler.get_uuids(app_id, 'apa', start, end)
    #
    # users_info = db_handler.get_uuids_info(app_id, *users)
    #
    # print users_info
    # print len(users_info)
    # num_men = 0
    # num_women = 0
    # num_unknown = 0
    # num_total = 0
    # num_friends = 0
    # avg_friends = 0
    #
    # for user in users_info:
    #     if user['g'] == 'm':
    #         num_men += 1
    #     elif user['g'] == 'f':
    #         num_women += 1
    #     elif user['g'] == 'u':
    #         num_unknown += 1
    #
    #     num_total += 1
    #     num_friends += user['f']
    #
    # avg_friends = num_friends / num_total
    # print num_men
    # print num_women
    # print num_unknown
    # print num_total
    # print num_friends
    # print avg_friends

    from insights.datapro.api import models
    import time

    base_result = models.BaseResult()

    print base_result.__dict__

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

    print '======================================================================'

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