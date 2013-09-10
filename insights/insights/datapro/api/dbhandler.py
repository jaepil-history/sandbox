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


    def get_column_values(self, app_id, collection_name, column_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")
        if column_name is None:
            raise Exception("Column name is not specified")

        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        app_info = self.get_app_info_from_appspand(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = collection.find({'_dt': {'$gte':start, '$lt':end}}).distinct(column_name)
        if result is None:
            raise Exception("No " +  column_name + "'s value found")

        return result


    def get_uuids(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        app_info = self.get_app_info_from_appspand(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = collection.find({'_dt': {'$gte':start, '$lt':end}}).distinct('uuid')
        if result is None:
            raise Exception("No uuid found")

        return result


    def find_dau(self, app_id, start, end):
        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        app_info = self.get_app_info_from_appspand(app_id)
        collection_name_items = [app_id, "event", "usr"]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = collection.find({'l_in': {'$gte':start, '$lt':end}})
        if result is None:
            raise Exception("Zero counted")

        return result


    def get_users_info_from_processed(self, app_id, *uuids):
        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        collection_name_items = [app_id, "processed", 'usr']
        canonical_collection_name = ".".join(collection_name_items)
        connection = self.connection["processed"]
        database = connection[self.dbs["config"].mongodb_processed_db_name]
        collection = database[canonical_collection_name]

        result = []
        for id in uuids:
            user = collection.find_one({'uuid':id})
            result.append(user)

        return result


    def get_user_info_from_processed(self, app_id, uuid):
        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        collection_name_items = [app_id, "processed", 'usr']
        canonical_collection_name = ".".join(collection_name_items)
        connection = self.connection["processed"]
        database = connection[self.dbs["config"].mongodb_processed_db_name]
        collection = database[canonical_collection_name]

        user_info = collection.find_one({'uuid':uuid})

        return user_info


    def update_user_retention_at_processed(self, app_id, uuid, days):
        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        collection_name_items = [app_id, "processed", 'ret']
        canonical_collection_name = ".".join(collection_name_items)
        connection = self.connection["processed"]
        database = connection[self.dbs["config"].mongodb_processed_db_name]
        collection = database[canonical_collection_name]

        result = collection.update( { "uuid": uuid },
                                    {
                                        # '$set': { 'ret.' + str(days - 1):True },
                                        '$inc': { 'ln.' + str(days - 1):1 }
                                    })

        return result


    def find_to_list(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        app_info = self.get_app_info_from_appspand(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = []
        cursor = collection.find({'_dt': {'$gte':start, '$lt':end}})
        for doc in cursor:
            result.append(doc)
        return result


    def find_from_insights(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        app_info = self.get_app_info_from_appspand(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        cursor = collection.find({'_dt': {'$gte':start, '$lt':end}})
        return cursor


    def insert_to_processed(self, app_id, collection_name, doc):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        if not isinstance(app_id, basestring):
            app_id = str(app_id)

        collection_name_items = [app_id, "processed", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["processed"]
        database = connection[self.dbs["config"].mongodb_processed_db_name]
        collection = database[canonical_collection_name]

        result = collection.insert(doc)
        return result

