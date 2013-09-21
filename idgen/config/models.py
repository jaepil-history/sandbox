# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

from mongoengine import Document
from mongoengine import EmbeddedDocument

from mongoengine import BooleanField
from mongoengine import EmbeddedDocumentField
from mongoengine import IntField
from mongoengine import ListField
from mongoengine import StringField


class Application(EmbeddedDocument):
    title = StringField(required=True)
    module = StringField(required=True)
    version = StringField(required=True)
    revision = IntField(required=True)
    stage = StringField(required=True)


class Logger(EmbeddedDocument):
    level = StringField(required=True)
    path = StringField(required=True)
    filename = StringField(required=True)


class Logging(EmbeddedDocument):
    access = EmbeddedDocumentField(Logger, required=True)
    application = EmbeddedDocumentField(Logger, required=True)
    general = EmbeddedDocumentField(Logger, required=True)


class HTTPServer(EmbeddedDocument):
    host = StringField(required=True)
    port = IntField(required=True)


class Security(EmbeddedDocument):
    ssl_cert = StringField()
    ssl_key = StringField()
    secret_key = StringField(required=True)


class MongoDB(EmbeddedDocument):
    alias = StringField(required=True)
    connection_uri = StringField(required=True)
    connection_pool = IntField(required=True)
    timeout = IntField(required=True)


class Redis(EmbeddedDocument):
    alias = StringField(required=True)
    enabled = BooleanField(required=True)
    connection_pool = IntField(required=True)
    timeout = IntField(required=True)
    host = StringField(required=True)
    port = IntField(required=True)
    password = StringField(required=True)
    db = IntField(required=True)


class Database(EmbeddedDocument):
    mongodb = ListField(EmbeddedDocumentField(MongoDB), required=True)
    redis = EmbeddedDocumentField(Redis, required=True)


class AppConfig(Document):
    application = EmbeddedDocumentField(Application, required=True)
    debug = BooleanField(required=True)
    logging = EmbeddedDocumentField(Logging, required=True)
    server = EmbeddedDocumentField(HTTPServer, required=True)
    security = EmbeddedDocumentField(Security, required=True)
    database = EmbeddedDocumentField(Database, required=True)
