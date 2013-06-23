# Copyright (c) 2013 Appspand, Inc.

from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import DateTimeField
from mongoengine import EmbeddedDocumentField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import StringField
from mongoengine import ListField

from mongoengine import blacklist
from mongoengine import whitelist


class Queue(Document):
    user_uid = StringField(required=True, max_length=512)
    message_uids = ListField(LongField())

    meta = {
        "indexes": [
            {"fields": ["user_uid"], "unique": True}
        ],
        "roles": {
            "json": {
                "_default": blacklist("id")
            }
        }
    }
