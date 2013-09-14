#from hashlib import sha256

from datetime import datetime, timedelta
import re

import tornado.escape
import tornado.gen
import tornado.web

import bson
import motor

import models


class BaseHandler(tornado.web.RequestHandler):
    class Context(object):
        def __init__(self, request):
            path = re.split("/", request.path)
            path = path[1:-1]

            self.arguments = {}
            for k, v in request.arguments.items():
                self.arguments[k] = v[0]
            self.full_path = path
            self.path = path
            self.type = path[0]
            self.version = path[1]
            self.app_id = path[2]
            self.function = path[3]

        def get_type(self):
            return self.type

        def get_app_id(self):
            return self.app_id

        def get_version(self):
            return self.version

        def get_function(self):
            return self.function

    class DBContext(object):
        def __init__(self, context, settings):
            self.context = context
            self.settings = settings
            self.connection = {
                "appspand": settings["db_client"]["appspand"],
                "insights": settings["db_client"]["insights"]
            }

        @tornado.gen.coroutine
        def get_app_info(self):
            connection = self.connection["appspand"]
            database = connection[self.settings["options"].mongodb_appspand_db_name]
            collection = database["application"]

            app_id = bson.ObjectId(self.context.get_app_id())
            doc = yield motor.Op(collection.find_one, {"_id": app_id})
            if doc is None:
                raise Exception("Application ID not found")

            app_info = models.ApplicationInfo(**doc)
            raise tornado.gen.Return(app_info)

        @tornado.gen.coroutine
        def get_user(self, collection_name, uuid, start=None, end=None):
            app_info = yield self.get_app_info()
            collection_name_items = [self.context.get_app_id(), "event", collection_name]
            canonical_collection_name = ".".join(collection_name_items)
            connection = self.connection["insights"]
            database = connection[app_info.cluster.db_name]
            collection = database[canonical_collection_name]

            doc = yield motor.Op(collection.find_one, {"uuid": uuid, '_dt': {'$gte':start, '$lt':end}})
            if doc is None:
                raise tornado.gen.Return(None)
                # raise Exception("User ID not found")

            user = models.User(**doc)
            raise tornado.gen.Return(user)

        @tornado.gen.coroutine
        def update_user(self, uuid, user_level, friends_count, last_login_at):
            app_info = yield self.get_app_info()
            collection_name_items = [self.context.get_app_id(), "event", "usr"]
            canonical_collection_name = ".".join(collection_name_items)

            connection = self.connection["insights"]
            database = connection[app_info.cluster.db_name]
            collection = database[canonical_collection_name]

            today = datetime.utcnow().date()
            diff_days = today - last_login_at.date()
            diff_days = diff_days.days
            diff_days = diff_days % models.MAX_RETENTION_DAYS

            result = yield motor.Op(collection.update, { "uuid": uuid },
                                    {
                                        '$set': { 'ul': user_level },
                                        '$set': { 'f': friends_count },
                                        '$set': { 'l_in': last_login_at },
                                        '$inc': { 'ln.' + str(diff_days - 1): 1 }
                                    }, multi=False)

            if result is None:
                raise Exception("User ID not found")

            raise tornado.gen.Return(result)

        @tornado.gen.coroutine
        def insert_legacy(self, app_info, doc):
            collection_name_items = [self.context.get_app_id(), "event", "all"]
            canonical_collection_name = ".".join(collection_name_items)

            connection = self.connection["insights"]
            database = connection[app_info.cluster.db_name]
            collection = database[canonical_collection_name]

            yield motor.Op(collection.insert, doc)

        @tornado.gen.coroutine
        def insert(self, collection_name, doc):
            if collection_name is None:
                raise Exception("Collection name is not specified")

            app_info = yield self.get_app_info()
            yield self.insert_legacy(app_info=app_info, doc=doc)

            collection_name_items = [self.context.get_app_id(), "event", collection_name]
            canonical_collection_name = ".".join(collection_name_items)

            connection = self.connection["insights"]
            database = connection[app_info.cluster.db_name]
            collection = database[canonical_collection_name]

            result = yield motor.Op(collection.insert, doc)

            raise tornado.gen.Return(result)

    def initialize(self):
        super(BaseHandler, self).initialize()

        self.options = self.settings["options"]
        self.context = self.Context(self.request)
        self.db_context = self.DBContext(context=self.context, settings=self.settings)


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

        # insert usr table for the first time login
        usr = models.User()
        usr.user_uid = apa.user_uid
        usr.friends_count = apa.friends_count
        usr.user_level = apa.user_level
        usr.created_at = apa.created_at
        usr.last_login_at = datetime.utcnow()
        yield usr.save(db_context=self.db_context, collection_name="usr", validate=True)

        # insert dau table for the first time login
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        start = datetime(today.year, today.month, today.day, 00, 00, 00)
        end = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00, 00)
        diff_days = (today - apa._dt.date()).days
        isExist = yield self.db_context.get_user('dau', apa.user_uid, start, end)
        if diff_days == 0 and isExist is None:
            dau = models.DAU()
            dau.user_uid = apa.user_uid
            dau.user_level = apa.user_level
            dau.friends_count = apa.friends_count
            yield dau.save(db_context=self.db_context, collection_name="dau", validate=True)

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

        # increase login count in usr collection, and update usr information
        uuid = cpu.user_uid
        user_level = cpu.user_level
        friends_count = cpu.friends_count
        last_login_at = cpu._dt
        yield self.db_context.update_user(uuid, user_level, friends_count, last_login_at)

        # insert dau table for the first time login
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        start = datetime(today.year, today.month, today.day, 00, 00, 00)
        end = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 00, 00, 00)
        diff_days = (today - cpu._dt.date()).days
        isExist = yield self.db_context.get_user('dau', cpu.user_uid, start, end)
        if diff_days == 0 and isExist is None:
            dau = models.DAU()
            dau.user_uid = cpu.user_uid
            dau.user_level = cpu.user_level
            dau.friends_count = cpu.friends_count
            yield dau.save(db_context=self.db_context, collection_name="dau", validate=True)

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