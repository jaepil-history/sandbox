#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from time import gmtime, strftime, sleep

#from insights.system import runner
import settings
from api.dbhandler import DBHandler
from pymongo import MongoClient
from datetime import datetime, timedelta, time
from processors import cal_nru_dau_retention
from processors import cal_pu_revenue


def init_database(config):
    mongodb_client = MongoClient(host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size)

    return mongodb_client


class DataProMain(object):

    def __init__(self, config):
        self.db_client = init_database(config=config)
        self.dbs = {
            "appspand": self.db_client,
            "insights": self.db_client,
            "processed": self.db_client,
            "config": config
        }
        self.db_handler = DBHandler(self.dbs)

    def run(self):

        while True:
            print 'datapro is running'
            print strftime("%Y-%m-%d %H:%M:%S", gmtime())
            print strftime("%a, %d %b %Y %X +0000", gmtime())

            # default : 24 hours ago
            today = datetime.utcnow().date()
            yesterday = today - timedelta(days=1)
            start = datetime.combine(yesterday, time())
            end = datetime.combine(today, time())

            # pymongo.run(self.db_handler)
            cal_nru_dau_retention.run(self.db_handler, start, end)
            cal_pu_revenue.run(self.db_handler, start, end)

            # Analyze data every single day
            # time.sleep(self.interval)
            # sleep(60 * 60 * 24)
            sleep(60 * 10)


def main():
    config = settings.parse_options()
    DataProMain(config=config).run()


if __name__ == "__main__":
    main()
