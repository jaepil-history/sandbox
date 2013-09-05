#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

try:
    import pymongo
except ImportError:
    pymongo = None


class DBHandler(object):
    def __init__(self, dbs):
        # self.app_id = app_id
        self.dbs = dbs
        self.connection = {
            "appspand": dbs["appspand"],
            "insights": dbs["insights"],
            "processed": dbs["processed"],
            "retention": dbs["retention"]
        }


    def get_app_ids(self):
        connection = self.connection["appspand"]
        database = connection[self.dbs["config"].mongodb_appspand_db_name]
        collection = database["application"]

        # selected = []
        # cursor = collection.find(fields=["_id", "name"])
        # for doc in cursor:
        #     selected.append({doc['name']:str(doc['_id'])})
        #
        # print selected

        result = collection.find().distinct("_id")
        if result is None:
            raise Exception("No application found")

        return result


    def get_app_info(self, app_id):
        connection = self.connection["appspand"]
        database = connection[self.dbs["config"].mongodb_appspand_db_name]
        collection = database["application"]

        app_info = collection.find_one(_id=app_id)
        if app_info is None:
            raise Exception("Application ID not found")

        return app_info


    def get_column_values(self, app_id, collection_name, column_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")
        if column_name is None:
            raise Exception("Column name is not specified")

        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = collection.find({'_dt': {'$gt':start, '$lte':end}}).distinct(column_name)
        if result is None:
            raise Exception("No " +  column_name + "'s value found")

        return result


    def get_uuids(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = collection.find({'_dt': {'$gt':start, '$lte':end}}).distinct('uuid')
        if result is None:
            raise Exception("No uuid found")

        return result


    def get_users_info(self, app_id, *uuids):
        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", 'cpu']
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = []
        for id in uuids:
            user = collection.find_one({'uuid':id})
            result.append(user)

        return result


    def get_user_info(self, app_id, uuid):
        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", 'cpu']
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        user_info = collection.find_one({'uuid':uuid})

        return user_info


    def find_to_list(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = []
        cursor = collection.find({'_dt': {'$gt':start, '$lte':end}})
        for doc in cursor:
            result.append(doc)
        return result


    def cursor(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        cursor = collection.find({'_dt': {'$gt':start, '$lte':end}})
        return cursor


    def insert(self, app_id, collection_name, doc):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        collection_name_items = [app_id, "processed", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["processed"]
        database = connection[self.dbs["config"].mongodb_processed_db_name]
        collection = database[canonical_collection_name]

        result = collection.insert(doc)
        return result

