# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

from mongoengine import EmbeddedDocument
from mongoengine import IntField
from mongoengine import ListField
from mongoengine import LongField
from mongoengine import StringField


class UniqueIDs(EmbeddedDocument):
    app_id = StringField(required=True, max_length=255)
    status = IntField(required=True)
    message = StringField(required=True, max_length=512)
    unique_ids = ListField(LongField())
