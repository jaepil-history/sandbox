#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from datetime import datetime, date, timedelta
import time

import bson
from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import DateTimeField
from mongoengine import EmbeddedDocumentField
from mongoengine import ObjectIdField
from mongoengine import IntField
from mongoengine import BooleanField
from mongoengine import LongField
from mongoengine import ListField
from mongoengine import StringField
from mongoengine import EmailField
from mongoengine import ValidationError
from password import PasswordField

MAX_LEVEL = 50
MAX_DAYS = 20

class BaseResult(Document):
    _dt = DateTimeField(required=True)
    title = StringField(required=True)
    timestamp = IntField(db_field='ts')
    last_doc_id = ObjectIdField(required=True, db_field='last_id')
    runtime = LongField(required=True)
    counts = IntField()


    def __init__(self, *args, **values):
        super(Document, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def to_python(self):
        data = self.to_mongo()
        data = bson.son.SON(data).to_dict()
        del(data['_cls'])
        return data

    def save(self, db_handler, collection_name, validate=False):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert(collection_name=collection_name, doc=doc)
        return result

    meta = {'allow_inheritance': True}


class UserDistributionByMinutes(BaseResult):

    level = ListField(IntField(), default=lambda: [0 for x in range(MAX_LEVEL)], db_field='lv')

    def __init__(self, interval=None, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        if interval is None:
            self.interval = timedelta(seconds=10*60)
        else:
            self.interval = timedelta(seconds=interval*60)

        self.start = self._dt - self.interval
        self.end = self._dt

    def groupbylevel(self, doc):
        try:
            self.level[doc['lv'] - 1] += 1
        except:
            print 'level is not proper'


class UserDistributionByMinutesByHour(BaseResult):
    pass


class UserDistributionByMinutesByDay(BaseResult):
    pass


class UserDistributionByMinutesByMonth(BaseResult):
    pass


class UserDistributionByMinutesByYear(BaseResult):
    pass


class NewUsersByDays(BaseResult):

    retention = ListField(BooleanField(), default=lambda: [False for x in range(MAX_DAYS)], db_field='ret')

    def __init__(self, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        self.retention[0] = True

    def setRetention(self, today):
        pass


class UserRetention(Document):

    _dt = DateTimeField(required=True)
    retention = ListField(BooleanField(), default=lambda: [False for x in range(300)], db_field='ret')

    def __init__(self, *args, **values):
        super(Document, self).__init__(*args, **values)
        self.retention[0] = True

    def setRetention(self, today):
        self.retention[today - self._dt] = True


class CustomEvent(Document):

    _dt = DateTimeField(required=True)
    uuid = LongField(required=True)
    name = StringField(required=True)
    value = LongField(required=True)

