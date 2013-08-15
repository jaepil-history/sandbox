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

from insights.datapro.core import settings


class DBHandler(object):
    def __init__(self, app_id, settings):
        self.app_id = app_id
        self.settings = settings
        self.connection = {
            "appspand": settings["database"]["appspand"],
            "insights": settings["database"]["insights"]
        }

    @tornado.gen.coroutine
    def get_app_ids(self):
        connection = self.connection["appspand"]
        database = connection[self.settings["options"].mongodb_appspand_db_name]
        collection = database["application"]

        ids = yield motor.Op(collection.find().to_list, {"_id"})
        if ids is None:
            raise Exception("No application found")

        raise tornado.gen.Return(ids)

    @tornado.gen.coroutine
    def get_app_info(self, app_id):
        connection = self.connection["appspand"]
        database = connection[self.settings["options"].mongodb_appspand_db_name]
        collection = database["application"]

        doc = yield motor.Op(collection.find_one, {"_id": app_id})
        if doc is None:
            raise Exception("Application ID not found")

        app_info = models.ApplicationInfo(**doc)
        raise tornado.gen.Return(app_info)

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

    @tornado.gen.coroutine
    def find(self, collection_name, start, end):
        if collection_name is None:
            raise Exception("Collection name is not specified")

        app_info = yield self.get_app_info()
        collection_name_items = [self.context.get_app_id(), "event", collection_name]
        canonical_collection_name = ".".join(collection_name_items)

        connection = self.connection["insights"]
        database = connection[app_info.cluster.db_name]
        collection = database[canonical_collection_name]

        result = yield motor.Op(collection.find().to_list, {'_dt': {'$gt':start, '$lte':end}})
        raise tornado.gen.Return(result)
        # cursor = yield motor.Op(collection.find, {'_dt': {'$gt':start, '$lte':end}})
        # while (yield cursor.fetch_next):
        #     doc = cursor.next_object()


class ApplicationAddedHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # kontagent = kontagent.Kontagent(
        #     app_id=self.options.kontagent_app_id,
        #     use_https=False,
        #     use_test_server=self.options.kontagent_use_test_server)
        # kontagent.track_application_added(**self.context.arguments)

        apa = models.ApplicationAdded(**self.context.arguments)
        yield apa.save(db_context=self.db_context, collection_name="apa", validate=True)
        self.write("1")
        self.finish()


class ApplicationRemovedHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        apr = models.ApplicationRemoved(**self.context.arguments)
        yield apr.save(db_context=self.db_context, collection_name="apr", validate=True)
        self.write("1")
        self.finish()


class UserInformationHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        cpu = models.UserInformation(**self.context.arguments)
        yield cpu.save(db_context=self.db_context, collection_name="cpu", validate=True)
        self.write("1")
        self.finish()


class CustomEventHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        evt = models.CustomEvent(**self.context.arguments)
        yield evt.save(db_context=self.db_context, collection_name="evt", validate=True)
        self.write("1")
        self.finish()


class InviteSentHandler(BaseHandler):
    pass


class InviteReceivedHandler(BaseHandler):
    pass


class GoalCountsHandler(BaseHandler):
    pass


class RevenueTrackingHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        mtu = models.RevenueTracking(**self.context.arguments)
        yield mtu.save(db_context=self.db_context, collection_name="mtu", validate=True)
        self.write("1")
        self.finish()


class PageRequestHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        pgr = models.PageRequest(**self.context.arguments)
        yield pgr.save(db_context=self.db_context, collection_name="pgr", validate=True)
        self.write("1")
        self.finish()


class StreamPostHandler(BaseHandler):
    pass


class StreamResponseHandler(BaseHandler):
    pass


class ExternalLinkClickHandler(BaseHandler):
    pass


class NotificationEmailSentHandler(BaseHandler):
    pass


class NotificationEmailResponseHandler(BaseHandler):
    pass