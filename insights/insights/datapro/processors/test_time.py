#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from datetime import datetime
from datetime import timedelta

print 5 % 28

today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

ref = '2013-09-01'
date_ref = datetime.date(ref)

print date_ref

print 'today: ' + str(today)
print 'yesterday: ' + str(yesterday)
print 'year: ' + str(today.year)
print 'month: ' + str(today.month)
print 'day: ' + str(today.day)





now = datetime.utcnow().today()
print now

prefix = ["%04d" % now.year,
            "%02d" % now.month,
            "%02d" % now.day]

col_prefix = "_".join(prefix)

print  col_prefix
print prefix

print now.timetuple()
print now.day

# print now.today()

# today = now.today()
# print today

hour = now.hour
print hour

minutes = now.minute
print minutes

interval = 10
td = timedelta(seconds = interval * 60)
print td

# for i in range(10):
#     print now - td * i

_dt = datetime.utcnow()
interval = 5

if interval is None:
    interval = timedelta(seconds=10*60)
else:
    interval = timedelta(seconds=interval*60)

start = _dt - interval
end = _dt

print 'start: ' + str(start)
print 'end: ' + str(end)

gender = ['m', 'f', 'u', 't']
ages = ['0-12', '13-17', '18-24', '25-29', '30-34', '35-39', '40-49', '50-59', '60-64', '65+', 't']
friends = ['0-10', '11-20', '21-40', '41-60', '61-80', '81-125', '126-249', '250+', 'u', 't']
country = ['Seoul', 'Busan', 'Incheon', 'Jeju', 'Jeonju', 'Daejeon', 'Daegu', 'Pohang', 'Gyeongju',
       'Jinju', 'Ulsan', 'Chuncheon', 'Anyang', 'Bucheon', 'Cheongju', 'Gumi', 'Gunsan', 'u', 't']

params = {
    'g': gender,
    'lc': country,
    'f': friends,
    'a': ages
}

g = [0 for x in range(len(gender))]
print g

from pymongo import MongoClient

db_client = MongoClient("mongodb://localhost:27017", max_pool_size=10)
# db_client = MongoClient(host='localhost', port=27017, max_pool_size=10)

database = db_client.appspand
collection = database.application

cursor = collection.find()

for doc in cursor:
    print doc

