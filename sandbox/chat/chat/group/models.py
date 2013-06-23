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


class group(Document):
    uid = StringField(required=True, max_length=512)
    title = StringField(max_length=512)
    owner = StringField(required=True, max_length=512)
    members = ListField(StringField(max_length=512), required=True)
    dt_created = IntField(required=True)

    meta = {
        # "indexes": [
        #     {"fields": ["uid"], "unique": True}
        # ],
        "roles": {
            "json": {
                "_default": blacklist("id", "dt_created")
            }
        }
    }
