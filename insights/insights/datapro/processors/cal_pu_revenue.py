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
        print 'calculating pu & revenue...'
        counts = 0
        last_doc_id = None
        start_cal = datetime.utcnow()

        usd_pu = models.PayingUsers('USD')
        kwn_pu = models.PayingUsers('KWN')
        #yen_pu = models.PayingUsers('YEN')

        # fix it when 2 months needed
        middle = ["%04d" % start.year, "%02d" % start.month]
        middle_name = ".".join(middle)

        query = {'_dt': {'$gte':start, '$lt':end }}
        usd_pu_ids = []
        kwn_pu_ids = []
        #yen_pu_ids = []

        for doc in db_handler.find_from_insights(app_id, middle_name, 'mtu', query):
            counts += 1

            if doc['cu'] == 0:
                usd_pu.revenue += doc['v']
                usd_pu.last_doc_id = doc['_id']
                if doc['uuid'] not in usd_pu_ids:
                    usd_pu_ids.append(doc['uuid'])
                    usd_pu.counts += 1
                    usd_pu.accumulate(doc)

            elif doc['cu'] == 1:
                kwn_pu.revenue += doc['v']
                kwn_pu.last_doc_id = doc['_id']
                if doc['uuid'] not in kwn_pu_ids:
                    kwn_pu_ids.append(doc['uuid'])
                    kwn_pu.counts += 1
                    kwn_pu.accumulate(doc)

            #elif doc['cu'] == 2:
            #    yen_pu.revenue += doc['v']
            #    yen_pu.last_doc_id = doc['_id']
            #    if doc['uuid'] not in yen_pu_ids:
            #        yen_pu_ids.append(doc['uuid'])
            #        yen_pu.counts += 1
            #        yen_pu.accumulate(doc)
            else:
                print 'currency is not defined'


        end_cal = datetime.utcnow()
        elapsed = (end_cal - start_cal).microseconds * 0.001

        usd_pu.runtime = elapsed
        kwn_pu.runtime = elapsed
        #yen_pu.runtime = elapsed

        #print usd_pu.to_python()
        #print kwn_pu.to_python()
        #print yen_pu.to_python()

        query = {"t": usd_pu.title, "currency": usd_pu.currency}
        usd_pu.upsert(db_handler, app_id, query)
        query = {"t": kwn_pu.title, "currency": kwn_pu.currency}
        kwn_pu.upsert(db_handler, app_id, query)
        #query = {"t": yen_pu.title, "currency": yen_pu.currency}
        #yen_pu.upsert(db_handler, app_id, query)


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