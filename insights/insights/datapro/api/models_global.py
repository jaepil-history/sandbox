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
from mongoengine import LongField
from mongoengine import ListField
from mongoengine import StringField
from mongoengine import EmailField
from mongoengine import ValidationError
from password import PasswordField


gender_division = ['m', 'f', 'u']
ages_division = ['0-12', '13-17', '18-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-64', '65+']
friends_division = ['0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'u']
country_division = ['Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
       'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'u']

# params = {
#     'g': gender_division,
#     'lc': country_division,
#     'f': friends_division,
#     'a': ages_division
# }

class BaseResult(Document):
    _dt = DateTimeField(required=True)
    title = StringField(required=True)
    timestamp = IntField(db_field='ts')
    last_doc_id = ObjectIdField(required=True, db_field='last_id')
    runtime = LongField(required=True)
    counts = IntField()
    gender = ListField(IntField(), default=lambda: [0 for x in range(len(gender_division))], db_field='g')
    ages = ListField(IntField(), default=lambda: [0 for x in range(len(ages_division))], db_field='a')
    friends = ListField(IntField(), default=lambda: [0 for x in range(len(friends_division))], db_field='f')
    country = ListField(IntField(), default=lambda: [0 for x in range(len(country_division))], db_field='lc')

    def __init__(self, *args, **values):
        super(Document, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.utcnow()
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def accumulate(self, doc):
        self.count_gender(doc)
        self.count_country(doc)
        self.count_ages(doc)
        self.count_friends(doc)

    def count_gender(self, doc):
        try:
            self.gender[gender_division.index(doc['g'])] += 1
        except:
            print 'gender value is not proper'

    def count_country(self, doc):
        try:
            self.country[country_division.index(doc['lc'])] += 1
        except:
            print 'country value is not proper'

    def count_ages(self, doc):
        age = date.today().year - int(doc['b'].split('/')[0])
        # print age
        for value in ages_division:
            if '-' in value:
                segment = value.split('-')
                start = int(segment[0])
                end = int(segment[1])
                if age >= start and age <= end:
                    self.ages[ages_division.index(value)] += 1
                    return

            elif '+' in value:
                segment = value.split('+')
                if age >= int(segment[0]):
                    self.ages[ages_division.index(value)] += 1
                    return

            else:
                print str(doc['_id']) + ': not counted by friends group'
                return

    def count_friends(self, doc):
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

    def __init__(self, interval=None, *args, **values):
        super(BaseResult, self).__init__(*args, **values)
        if interval is None:
            self.interval = timedelta(seconds=10*60)
        else:
            self.interval = timedelta(seconds=interval*60)

        self.start = self._dt - self.interval
        self.end = self._dt

    def count(self):
        pass


class UserDistributionByMinutesByHour(BaseResult):
    pass


class UserDistributionByMinutesByDay(BaseResult):
    pass


class UserDistributionByMinutesByMonth(BaseResult):
    pass


class UserDistributionByMinutesByYear(BaseResult):
    pass

