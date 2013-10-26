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


PLATFORM_UNKNOWN = 0
PLATFORM_MOBILE_IOS = 10001
PLATFORM_MOBILE_ANDROID = 10002
PLATFORM_DESKTOP_OSX = 20001
PLATFORM_DESKTOP_LINUX = 20002
PLATFORM_DESKTOP_WINDOWS = 20003


class DeviceInfo(EmbeddedDocument):
    platform_id = IntField(required=True)
    device_token = StringField(required=True, max_length=512)


class User(Document):
    uid = StringField(required=True, max_length=512)
    name = StringField(required=True, max_length=255)
    devices = ListField(EmbeddedDocumentField(DeviceInfo))
    joined_groups = ListField(StringField(max_length=512))
    created_at = DateTimeField(required=True)
    last_login_at = DateTimeField(required=True)

    meta = {
        "indexes": [
            {"fields": ["uid"], "unique": True}
        ],
        "roles": {
            "json": {
                "_default": blacklist("id", "devices", "created_at", "last_login_at")
            }
        }
    }
