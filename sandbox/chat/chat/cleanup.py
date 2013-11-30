#!/usr/bin/env python
#
# Copyright (c) 2013 Appspand, Inc.

import sys

import mongoengine

import app.config
from log import logger
import message.models
import queue.models
from util import cache


def build_url_handlers():
    from message import urls as message_urls
    from net.websocket import urls as ws_urls
    from group import urls as group_urls
    from user import urls as user_urls

    handlers = message_urls.handlers + ws_urls.handlers\
        + group_urls.handlers + user_urls.handlers

    return handlers


def init_database(config):
    database = config.database

    redis = database.redis
    if redis.enabled:
        cache.init(host=redis.host, port=redis.port,
                   password=redis.password, pool_size=redis.connection_pool,
                   socket_timeout=redis.timeout, db=redis.db)

        redis = cache.get_connection()
        redis.ping()

    mongodb = database.mongodb
    mongoengine.connect(db="chat",
                        host=mongodb.connection_uri,
                        max_pool_size=mongodb.connection_pool,
                        socketTimeoutMS=mongodb.timeout)
    logger.access.debug("mongodb connection url: %s" % mongodb.connection_uri)


def flush_queue(config):
    queue_rows = queue.models.Queue.objects()
    count = 0
    for row in queue_rows:
        messages = message.models.Message.objects(uid__in=row.message_uids)
        expired_muids = []
        count += 1
        print count, row.user_uid, len(row.message_uids), len(messages)
        for muid in row.message_uids:
            found = False
            for msg in messages:
                if msg.uid == muid:
                    found = True
                    break

            if not found:
                expired_muids.append(muid)
        for muid in expired_muids:
            row.message_uids.remove(muid)

        row.save()


def main():
    logger.init()

    if len(sys.argv) < 2:
        print "main.py [config]"
        return False

    config = app.config.load_appcfg(sys.argv[1])

    init_database(config=config)
    flush_queue(config=config)

    return 0


if __name__ == "__main__":
    main()
