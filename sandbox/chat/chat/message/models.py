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


class Message(Document):
    uid = IntField(required=True)
    room_uid = StringField(required=True, max_length=512)
    user_uid = StringField(required=True, max_length=512)
    message = StringField(required=True, max_length=1024)
    countdown = IntField(required=True)
    issued_at = IntField(required=True)
    expires_at = IntField(required=True)

    meta = {
        # "indexes": [
        #     {"fields": ["uid"], "unique": True}
        # ],
        "roles": {
            "json": {
                "_default": blacklist("id")
            }
        }
    }
