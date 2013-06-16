# Copyright (c) 2013 Appspand, Inc.

from __future__ import absolute_import

from mq.celery import celery

@celery.task
def add(x, y):
    return x + y
