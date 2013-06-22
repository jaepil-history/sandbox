# Copyright (c) 2013 Doobic Game Studios, Inc.

from datetime import datetime
import time


def get_timestamp(t=None):
    if t is None:
        t = int(round(time.time()))

    if isinstance(t, datetime):
        return int(time.mktime(t.timetuple()))
    elif isinstance(t, time.struct_time):
        return int(time.mktime(t))

    return int(t)


def get_datetime(ts):
    return datetime.utcfromtimestamp(ts)
