#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from datetime import datetime, timedelta
import time

import bson
from mongoengine import Document
from mongoengine import DateTimeField
from mongoengine import ObjectIdField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import FloatField
from mongoengine import StringField
from mongoengine import ListField
from mongoengine import DictField
from mongoengine import ValidationError

MAX_LEVEL = 100
MAX_RETENTION_DAYS = 28

friends_division = ['0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'u']

class BaseResult(Document):
    _dt = DateTimeField(required=True)
    title = StringField(required=True, db_field='t')
    timestamp = IntField(db_field='ts')
    last_doc_id = ObjectIdField(db_field='l_id') # for reference, not necessary. if doc's count = 0, last_doc_id = None
    runtime = LongField(required=True)
    counts = IntField()
    level = ListField(IntField(), default=lambda: [0 for x in range(MAX_LEVEL)], db_field='lv')
    friends = ListField(IntField(), default=lambda: [0 for x in range(len(friends_division))], db_field='f')

    def __init__(self, *args, **values):
        super(Document, self).__init__(*args, **values)
        self.initialize()


    def initialize(self):
        self._dt = datetime.utcnow()
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())


    def group_by_level(self, doc):
        try:
            self.level[doc['ul'] - 1] += 1
        except:
            print 'user level is not proper'


    def group_by_friends(self, doc):
        position = doc['f']
        for value in friends_division:
            if '-' in value:
                segment = value.split('-')
                start = int(segment[0])
                end = int(segment[1])
                if position >= start and position <= end:
                    self.friends[friends_division.index(value)] += 1
                    break

            elif '+' in value:
                segment = value.split('+')
                if position >= int(segment[0]):
                    self.friends[friends_division.index(value)] += 1
                    break

            elif value == 'u':
                self.friends[friends_division.index(value)] += 1
                break

            else:
                print str(doc['_id']) + ': not counted by friends group'


    def to_python(self):
        data = self.to_mongo()
        data = bson.son.SON(data).to_dict()
        del(data['_cls'])
        return data


    def save(self, db_handler, app_id, collection_name, validate=False):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert_to_processed(app_id=app_id, collection_name=collection_name, doc=doc)
        return result

    def upsert(self, db_handler, app_id, collection_name, query, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.upsert_to_processed(app_id=app_id, collection_name=collection_name, query=query, doc=doc)
        return result

    meta = {'allow_inheritance': True}


# new users distribution by friends count
class NRUDistribution(BaseResult):

    def __init__(self, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        yesterday = self._dt.date() - timedelta(days=1)
        self.title = str(yesterday)
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def accumulate(self, doc):
        self.group_by_friends(doc)

    def to_python(self):
        data = self.to_mongo()
        data = bson.son.SON(data).to_dict()
        del(data['_cls'])
        del(data['lv'])
        return data

    def save(self, db_handler, app_id, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert_to_processed(app_id=app_id, collection_name='installs', doc=doc)
        return result

    def upsert(self, db_handler, app_id, query, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.upsert_to_processed(app_id=app_id, collection_name='installs', query=query, doc=doc)
        return result


# daily access users distribution by friends count and by level
class DAUDistribution(BaseResult):

    def __init__(self, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        yesterday = self._dt.date() - timedelta(days=1)
        self.title = str(yesterday)
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def accumulate(self, doc):
        self.group_by_friends(doc)
        self.group_by_level(doc)

    def save(self, db_handler, app_id, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert_to_processed(app_id=app_id, collection_name='dau', doc=doc)
        return result

    def upsert(self, db_handler, app_id, query, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.upsert_to_processed(app_id=app_id, collection_name='dau', query=query, doc=doc)
        return result


class UserRetention(Document):

    _dt = DateTimeField(required=True)
    title = StringField(required=True, db_field='t')
    new_users = IntField(required=True, db_field='nu')
    timestamp = IntField(db_field='ts')
    retention = ListField(FloatField(), default=lambda: [0 for x in range(MAX_RETENTION_DAYS)], db_field='ret')

    def __init__(self, *args, **values):
        super(Document, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        self.start_date = self._dt.date() - timedelta(days=1)
        self.title = str(self.start_date)
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def to_python(self):
        data = self.to_mongo()
        data = bson.son.SON(data).to_dict()
        return data

    def set_retention(self, db_handler, app_id, usr):
        pass

    def save(self, db_handler, app_id, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert_to_processed(app_id=app_id, collection_name='retention', doc=doc)
        return result

    def upsert(self, db_handler, app_id, query, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.upsert_to_processed(app_id=app_id, collection_name='retention', query=query, doc=doc)
        return result


# revenue distribution by friends count and by level
class Revenue(BaseResult):
    item_list = ListField(IntField(), db_field='items')
    # currency. USD:0, KWN:1, YEN:2,
    currency = [0, 1, 2]

    def __init__(self, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        yesterday = self._dt.date() - timedelta(days=1)
        self.title = str(yesterday)
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def accumulate(self, doc):
        self.group_by_friends(doc)
        self.group_by_level(doc)

    def save(self, db_handler, app_id, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert_to_processed(app_id=app_id, collection_name='pu', doc=doc)
        return result

    def upsert(self, db_handler, app_id, query, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.upsert_to_processed(app_id=app_id, collection_name='pu', query=query, doc=doc)
        return result


# selling items(paying by game money) distribution by friends count and by level
class ItemsDistribution(BaseResult):
    items = DictField(db_field='items')

    def __init__(self, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        yesterday = self._dt.date() - timedelta(days=1)
        self.title = str(yesterday)
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def accumulate(self, doc):
        self.group_by_friends(doc)
        self.group_by_level(doc)

    def save(self, db_handler, app_id, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert_to_processed(app_id=app_id, collection_name='items', doc=doc)
        return result

    def upsert(self, db_handler, app_id, query, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.upsert_to_processed(app_id=app_id, collection_name='items', query=query, doc=doc)
        return result


# paying users distribution by friends count and by level
class PUDistribution(BaseResult):
    item_list = ListField(IntField(), db_field='items')
    # currency. USD:0, KWN:1, YEN:2,
    currency = [0, 1, 2]

    def __init__(self, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        yesterday = self._dt.date() - timedelta(days=1)
        self.title = str(yesterday)
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def accumulate(self, doc):
        self.group_by_friends(doc)
        self.group_by_level(doc)

    def save(self, db_handler, app_id, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.insert_to_processed(app_id=app_id, collection_name='pu', doc=doc)
        return result

    def upsert(self, db_handler, app_id, query, validate=True):
        if validate:
            try:
                self.validate()
            except ValidationError:
                print 'result validation error.'
                print ValidationError.to_dict()

        doc = self.to_python()
        result = db_handler.upsert_to_processed(app_id=app_id, collection_name='pu', query=query, doc=doc)
        return result


class CustomEvent(Document):

    _dt = DateTimeField(required=True)
    uuid = LongField(required=True)
    name = StringField(required=True)
    value = LongField(required=True)

