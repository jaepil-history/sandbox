# Copyright (c) 2013 Appspand, Inc.

import json
import yaml

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


class HostName(EmbeddedDocument):
    host = StringField(required=True)


class HTTPServer(EmbeddedDocument):
    hosts = ListField(EmbeddedDocumentField(HostName), required=True)
    base_port = IntField(required=True)


class MongoDB(EmbeddedDocument):
    connection_uri = StringField(required=True)
    connection_pool = IntField(required=True)
    timeout = IntField(required=True)


class Redis(EmbeddedDocument):
    enabled = BooleanField(required=True)
    connection_pool = IntField(required=True)
    timeout = IntField(required=True)
    host = StringField(required=True)
    port = IntField(required=True)
    password = StringField(required=True)
    db = IntField(required=True)


class Database(EmbeddedDocument):
    mongodb = EmbeddedDocumentField(MongoDB, required=True)
    redis = EmbeddedDocumentField(Redis, required=True)


class Session(EmbeddedDocument):
    timeout_minutes = IntField(required=True)


class AmazonSQS(EmbeddedDocument):
    access_key = StringField(required=True)
    secret_key = StringField(required=True)
    region = StringField(required=True)
    path = StringField(required=True)
    request_queue_name = StringField(required=True)
    fallback_queue_name = StringField(required=True)


class Interop(EmbeddedDocument):
    sqs = EmbeddedDocumentField(AmazonSQS)


class AppConfig(Document):
    application = EmbeddedDocumentField(Application, required=True)
    debug = BooleanField(required=True)
    logging = EmbeddedDocumentField(Logging, required=True)
    server = EmbeddedDocumentField(HTTPServer, required=True)
    database = EmbeddedDocumentField(Database, required=True)
    session = EmbeddedDocumentField(Session, required=True)
    interop = EmbeddedDocumentField(Interop)


options = None
appcfg = None


def load_appcfg(filename):
    global appcfg
    opt = yaml.load(file(filename))
    appcfg = AppConfig.from_json(json.dumps(opt))
    return appcfg
