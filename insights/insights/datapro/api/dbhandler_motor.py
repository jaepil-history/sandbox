#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

try:
    import motor
except ImportError:
    motor = None

import re

import tornado.escape
import tornado.gen
import tornado.web

import bson
import models


class DBHandler(object):
    def __init__(self, dbs):
        # self.app_id = app_id
        self.dbs = dbs
        self.connection = {
            "appspand": dbs["appspand"],
            "insights": dbs["insights"],
            "processed" : dbs["processed"]
        }


    @tornado.gen.coroutine
    def get_app_ids(self):
        connection = self.connection["appspand"]
        database = connection[self.dbs["config"].mongodb_appspand_db_name]
        collection = database["application"]

        print collection
        ids = yield motor.Op(collection.find, {"_id"})
        print ids
        if ids is None:
            raise Exception("No application found")

        raise tornado.gen.Return(ids)


    @tornado.gen.coroutine
    def get_app_info(self, app_id):
        connection = self.connection["appspand"]
        database = connection[self.dbs["config"].mongodb_appspand_db_name]
        collection = database["application"]

        app_info = yield motor.Op(collection.find_one, {"_id": app_id})
        if app_info is None:
            raise Exception("Application ID not found")

        raise tornado.gen.Return(app_info)


    @tornado.gen.coroutine
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

        result = yield motor.Op(collection.find({'_dt': {'$gt':start, '$lte':end}}).distinct, column_name)
        if result is None:
            raise Exception("No " +  column_name + "'s value found")

        raise tornado.gen.Return(result)


    @tornado.gen.coroutine
    def get_uuids(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = yield motor.Op(collection.find({'_dt': {'$gt':start, '$lte':end}}).distinct, 'uuid')
        if result is None:
            raise Exception("No uuid found")

        raise tornado.gen.Return(result)


    @tornado.gen.coroutine
    def get_users_info(self, app_id, *uuids):
        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", 'cpu']
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = []
        for id in uuids:
            user = yield motor.Op(collection.find_one({'uuid':id}))
            result.append(user)

        raise tornado.gen.Return(result)


    @tornado.gen.coroutine
    def get_user_info(self, app_id, uuid):
        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", 'cpu']
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        user_info = yield motor.Op(collection.find_one, {'uuid':uuid})
        raise tornado.gen.Return(user_info)


    @tornado.gen.coroutine
    def find_to_list(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        result = yield motor.Op(collection.find().to_list, {'_dt': {'$gt':start, '$lte':end}})
        raise tornado.gen.Return(result)
        # cursor = yield motor.Op(collection.find, {'_dt': {'$gt':start, '$lte':end}})
        # while (yield cursor.fetch_next):
        #     doc = cursor.next_object()


    @tornado.gen.coroutine
    def cursor(self, app_id, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = self.get_app_info(app_id)
        collection_name_items = [app_id, "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info['cluster']['db_name']]
        collection = database[canonical_collection_name]

        cursor = yield motor.Op(collection.find, {'_dt': {'$gt':start, '$lte':end}})
        raise tornado.gen.Return(cursor)

        # cursor = db.messages.find().sort([('_id', -1)])
        # while (yield cursor.fetch_next):
        #     message = cursor.next_object()



    @tornado.gen.coroutine
    def insert(self, collection_name, doc):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = yield self.get_app_info(app_id=self.app_id)
        collection_name_items = [self.app_id, "processed", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info.cluster.db_name]
        collection = database[canonical_collection_name]

        result = yield motor.Op(collection.insert, doc)
        raise tornado.gen.Return(result)