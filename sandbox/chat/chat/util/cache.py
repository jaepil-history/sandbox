# Copyright (c) 2013 Appspand, Inc.

from redis import ConnectionPool
from redis import Redis


def init(host="localhost", port=6379, password=None, pool_size=None, db=0, **kwargs):
    global connection_pool

    if len(password) == 0:
        password = None

    connection_pool = ConnectionPool(host=host, port=port,
                                     password=password,
                                     max_connections=pool_size,
                                     db=db, **kwargs)


def get_pool():
    global connection_pool
    return connection_pool


def get_connection():
    global connection_pool
    return Redis(connection_pool=connection_pool)
