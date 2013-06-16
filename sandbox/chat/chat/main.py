#!/usr/bin/env python
#
# Copyright (c) 2013 Appspand, Inc.

import mongoengine

# from celery import Celery

from tornado import httpserver
from tornado import ioloop
from tornado import web

from settings import base
from util import cache


config = base.parse_options()
# celery = Celery(main="chat.mq", broker=config.celery_broker_url,
#                 backend=config.celery_result_backend_url)


# class User:
#     user_id = ""
#     data = ""
#
#
# class Message:
#     message_id = ""
#     data = ""
#     read_count = 0
#
#
# class Room:
#     room_id = ""
#     user_list = []
#     message_queue = []
#
#
# class Chat:
#     def invite(self):
#         pass
#
#     def join(self):
#         pass
#
#     def leave(self):
#         pass
#
#     def send(self):
#         pass
#
#     def read(self):
#         pass


class Application(web.Application):
    pass


def build_url_handlers():
    from message import urls as message_urls
    from room import urls as room_urls
    from user import urls as user_urls
    from ws import urls as ws_urls

    # fav_icon_handler = [(r"/(favicon.ico)", None)]
    handlers = message_urls.handlers + room_urls.handlers + user_urls.handlers + ws_urls.handlers

    return handlers


def init_database(config):
    cache.init(host=config.redis_host, port=config.redis_port,
               password=config.redis_password, pool_size=config.redis_pool_size,
               socket_timeout=config.redis_timeout, db=config.redis_db)

    redis = cache.get_connection()
    redis.ping()

    mongoengine.connect(db="chat",
                        host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size,
                        socketTimeoutMS=config.mongodb_timeout)


def init_http_server(config):
    url_handlers = build_url_handlers()
    application = Application(
        handlers=url_handlers,
        options=config
    )
    application.add_handlers(config.host, url_handlers)

    http_server = httpserver.HTTPServer(application)
    http_server.listen(config.port)


def run_server(config):
    ioloop.IOLoop.instance().start()


def main():
    init_database(config=config)

    init_http_server(config=config)

    run_server(config=config)

    return 0


if __name__ == "__main__":
    main()
