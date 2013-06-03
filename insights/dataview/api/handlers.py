#from hashlib import sha256

import re

import tornado.escape
import tornado.gen
import tornado.web

import bson
import motor
from dataview.api import models

#from ..proxy import kontagent


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
                "appspand": settings["database"]["appspand"],
                "insights": settings["database"]["insights"]
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


'''
'''

class DiscoveryHandler(BaseHandler):
    pass


class EmailConversionHandler(BaseHandler):
    pass


class EmailEventsHandler(BaseHandler):
    pass


class EmailLimitHandler(BaseHandler):
    pass


class EmailsReceivedHandler(BaseHandler):
    pass


class EmailsResponsesHandler(BaseHandler):
    pass


class EmailsSentHandler(BaseHandler):
    pass


class InviteConversionHandler(BaseHandler):
    pass


class InviteEventsHandler(BaseHandler):
    pass


class InviteLimitHandler(BaseHandler):
    pass


class InvitesReceivedHandler(BaseHandler):
    pass


class InviteResponsesHandler(BaseHandler):
    pass


class InvitesSentHandler(BaseHandler):
    pass


class MessagesSentHandler(BaseHandler):
    pass


class MessagesClicksHandler(BaseHandler):
    pass


class MessagesResponsesHandler(BaseHandler):
    pass


class NotificationConversionHandler(BaseHandler):
    pass


class NotificationEventsHandler(BaseHandler):
    pass


class NotificationLimitHandler(BaseHandler):
    pass


class NotificationsSentHandler(BaseHandler):
    pass


class NotificationsReceivedHandler(BaseHandler):
    pass


class NotificationsResponsesHandler(BaseHandler):
    pass


class StreamPostHandler(BaseHandler):
    pass


class StreamResponseHandler(BaseHandler):
    pass


class ExternalLinkClickHandler(BaseHandler):
    pass


class StreamPostClickRatioHandler(BaseHandler):
    pass


class MonetizationRevenueHandler(BaseHandler):
    pass


class MonetizationTransactionsHandler(BaseHandler):
    pass


class MonetizationAverageTransactionHandler(BaseHandler):
    pass


class MonetizationARPPUHandler(BaseHandler):
    pass


class MonetizationSpendingUsersHandler(BaseHandler):
    pass


class TrafficClicksHandler(BaseHandler):
    pass


class TrafficInstallSummaryHandler(BaseHandler):
    pass


class TrafficInstallsHandler(BaseHandler):
    pass


class TrafficSummaryHandler(BaseHandler):
    pass


class EventsCountHandler(BaseHandler):
    pass


class EventsDistributionHandler(BaseHandler):
    pass


class EventsNamesHandler(BaseHandler):
    pass


class EventsNamesSubtreeHandler(BaseHandler):
    pass


class EventsValueHandler(BaseHandler):
    pass


class GoalCountsHandler(BaseHandler):
    pass


class PageViewsHandler(BaseHandler):
    pass


class UsersGenderDistributionHandler(BaseHandler):
    pass


class UsersAgeDistributionHandler(BaseHandler):
    pass


class UsersFriendsDistributionHandler(BaseHandler):
    pass


class UsersCountryDistributionHandler(BaseHandler):
    pass


class UsersViralityHandler(BaseHandler):
    pass


class UsersReturningUsersHandler(BaseHandler):
    pass


class UsersUniqueVisitorsHandler(BaseHandler):
    pass


class UsersUniqueRollingHandler(BaseHandler):
    pass


class UsersRetentionHandler(BaseHandler):
    pass


class InstallsAllHandler(BaseHandler):
    pass


class InstallsUniqueHandler(BaseHandler):
    pass


class RemovesHandler(BaseHandler):
    pass


class UserSessionsHandler(BaseHandler):
    pass


class UserSessionsHandler(BaseHandler):
    pass