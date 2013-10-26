# Copyright (c) 2013 Appspand, Inc.

from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import BooleanField
from mongoengine import DateTimeField
from mongoengine import EmbeddedDocumentField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import StringField
from mongoengine import ListField

from mongoengine import blacklist
from mongoengine import whitelist


class Message(Document):
    uid = LongField(required=True)
    sender_uid = StringField(required=True, max_length=512)
    group_uid = StringField(max_length=512)
    message = StringField(required=True, max_length=10240)
    countdown = IntField(required=True)
    issued_at = DateTimeField(required=True)
    expires_at = DateTimeField(required=True)
    is_secret = BooleanField(default=False)
    recipient_count = IntField(default=0)
    unveil_count = IntField(default=0)

    meta = {
        "indexes": [
            {"fields": ["uid"], "unique": True},
            {"fields": ["issued_at"], "expireAfterSeconds": 1 * 60 * 60 * 24 * 7}
        ],
        "roles": {
            "json": {
                "_default": blacklist("id")
            }
        }
    }
