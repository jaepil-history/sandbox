#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

try:
    import pymongo
except ImportError:
    pymongo = None

from datetime import datetime
from datetime import timedelta

class DBHandler(object):
    def __init__(self, dbs):
        # self.app_id = app_id
        self.dbs = dbs
        self.connection = {
            "appspand": dbs["appspand"],
            "insights": dbs["insights"],
            "processed": dbs["processed"]
        }


    def get_app_ids_from_appspand(self):
        connection = self.connection["appspand"]
        database = connection[self.dbs["config"].mongodb_appspand_db_name]
        collection = database["application"]

        result = collection.find().distinct("_id")
        if result is None:
            raise Exception("No application found")

        return result


    def get_app_info_from_appspand(self, app_id):
        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        connection = self.connection["appspand"]
        database = connection[self.dbs["config"].mongodb_appspand_db_name]
        collection = database["application"]

        app_info = collection.find_one(_id=app_id)
        if app_info is None:
            raise Exception("Application ID not found")

        return app_info


    def find_from_insights(self, app_id, year_month, collection_name, query=None):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        app_info = self.get_app_info_from_appspand(app_id)
        collection_name_items = [app_id, year_month, collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        cursor = collection.find(query)
        return cursor


    def find_from_usr(self, app_id, query=None):
        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        app_info = self.get_app_info_from_appspand(app_id)
        collection_name_items = [app_id, 'usr']
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        cursor = collection.find(query)
        return cursor


    def find_from_processed(self, app_id, collection_name, query=None):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        collection_name_items = [app_id, collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["processed"]
        database = connection[self.dbs["config"].mongodb_processed_db_name]
        collection = database[canonical_collection_name]

        cursor = collection.find(query)
        return cursor