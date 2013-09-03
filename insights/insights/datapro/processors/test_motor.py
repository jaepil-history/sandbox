#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

from insights.datapro import settings

from motor import MotorClient
from insights.datapro.api.dbhandler_motor import DBHandler

def init_database(config):
    mongodb_client = MotorClient(
        config.mongodb_connection_uri,
        max_concurrent=config.mongodb_max_concurrent,
        max_wait_time=config.mongodb_max_wait_time
    ).open_sync()

    return mongodb_client

config = settings.parse_options()
db_client = init_database(config=config)
dbs = {
    "appspand": db_client,
    "insights": db_client,
    "processed": db_client,
    "config": config
}

db_handler = DBHandler(dbs)
print db_handler

app_ids = db_handler.get_app_ids()

print app_ids




from datetime import datetime, timedelta

start = datetime.utcnow() - timedelta(hours=250)
end = datetime.utcnow()
app_id = "520472e035b6e6185caf70dc"

print app_id
print start
print end

# for doc in db_handler.cursor(app_id, 'cpu', start, end):
#     print doc

print '==============================================================='

result = db_handler.find_to_list(app_id, 'apa', start, end)
print result
print db_handler.get_column_values(app_id, 'apa', 'uuid', start, end)

users = db_handler.get_uuids(app_id, 'apa', start, end)
users_info = db_handler.get_users_info(app_id, *users)
print users_info
print len(users_info)

# num_men = 0
# num_women = 0
# num_unknown = 0
# num_total = 0
# num_friends = 0
# avg_friends = 0
#
# for user in users_info:
#     if user['g'] == 'm':
#         num_men += 1
#     elif user['g'] == 'f':
#         num_women += 1
#     elif user['g'] == 'u':
#         num_unknown += 1
#
#     num_total += 1
#     num_friends += user['f']
#
# avg_friends = num_friends / num_total
# print num_men
# print num_women
# print num_unknown
# print num_total
# print num_friends
# print avg_friends

from insights.datapro.api import models
import time

base_result = models.BaseResult()

print base_result.__dict__

counts = 0
elapsed = 0
last_doc_id = None
start_cal = time.time()

users = db_handler.find_to_list(app_id, 'cpu', start, end)
print 'users'
print users

# while True:
#     if not cursor.alive:
#         # While collection is empty, tailable cursor dies immediately
#         yield gen.Task(loop.add_timeout, datetime.timedelta(seconds=1))
#         cursor = capped.find(tailable=True, await_data=True)
#
#     if (yield cursor.fetch_next):
#         results.append(cursor.next_object())
#
# while yield cursor.fetch_next():
#     doc = cursor.next_object()
#
# for doc in users:
#     counts += 1
#     last_doc_id = doc['_id']
#     base_result.accumulate(doc)
#
# print 'last_doc_id = ' + str(last_doc_id)
#
# end_cal = time.time()
# elapsed = (end_cal - start_cal) * 1000
# print 'time to read db: ' + str(elapsed) + 'msec'
# print 'counted items: ' + str(counts)
#
# base_result.last_doc_id = last_doc_id
# base_result.title = 'user_distribution'
# base_result.runtime = elapsed
# base_result.timestamp = int(time.time())
# base_result.counts = counts
#
# print base_result.__dict__
# print base_result.to_python()
#
# print '======================================================================'
#
# base_result1 = models.BaseResult()
#
# print base_result1.__dict__
#
# counts = 0
# elapsed = 0
# last_doc_id = None
# start_cal = time.time()
#
# memory = db_handler.find_to_list(app_id, 'cpu', start, end)
#
# for doc in memory:
#     counts += 1
#     last_doc_id = doc['_id']
#     base_result1.accumulate(doc)
#
# print 'last_doc_id = ' + str(last_doc_id)
#
# end_cal = time.time()
# elapsed = (end_cal - start_cal) * 1000
# print 'time to read db: ' + str(elapsed) + 'msec'
# print 'counted items: ' + str(counts)
#
# base_result1.last_doc_id = last_doc_id
# base_result1.title = 'user_distribution'
# base_result1.runtime = elapsed
# base_result1.timestamp = int(time.time())
# base_result1.counts = counts
#
# print base_result1.__dict__
# print base_result1.to_python()
#
#
#
