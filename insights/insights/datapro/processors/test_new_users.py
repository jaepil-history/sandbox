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
    app_ids = db_handler.get_app_ids_from_appspand()

    print app_ids

    from datetime import datetime, timedelta

    start = datetime.utcnow().today() - timedelta(hours=1000)
    end = datetime.utcnow().today()
    app_id = "5226e79b35b6e6080cca3f1d"
    # app_id = "5226e77335b6e61184d73e39"

    print app_id
    print start
    print end

    from insights.datapro.api import models
    import time

    print 'saving nru ...'
    counts = 0
    elapsed = 0
    last_doc_id = None
    start_cal = time.time()

    for doc in db_handler.find_from_insights(app_id, 'apa', start, end):
        counts += 1
        last_doc_id = doc['_id']
        user = models.User()
        user.created_at = doc['c']
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
    run(db_handler=db_handler)