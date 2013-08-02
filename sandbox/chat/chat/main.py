#!/usr/bin/env python
#
# Copyright (c) 2013 Appspand, Inc.

import signal
import sys
import time

# import daemonize

import mongoengine

# from celery import Celery

from tornado import httpserver
from tornado import ioloop
from tornado import web

from net.tcp import acceptor
from settings import base
from util import cache


config = base.parse_options()


def shutdown():
    io_loop = ioloop.IOLoop.instance()

    # io_loop.tcp_server.stop()

    # logging.info('Will shutdown in 2 seconds ...')
    io_loop.add_timeout(time.time() + 2, io_loop.stop)


def sig_handler(sig, frame):
    """Catch signal and init callback.

    More information about signal processing for graceful stopping
    Tornado server you can find here:
    http://codemehanika.org/blog/2011-10-28-graceful-stop-tornado.html
    """

    io_loop = ioloop.IOLoop.instance()

    # logging.warning('Caught signal: %s', sig)

    ioloop.IOLoop.instance().add_callback(shutdown)


class Application(web.Application):
    pass


def build_url_handlers():
    from message import urls as message_urls
    from net.websocket import urls as ws_urls
    from group import urls as group_urls
    from user import urls as user_urls

    # fav_icon_handler = [(r"/(favicon.ico)", None)]
    handlers = message_urls.handlers + ws_urls.handlers\
        + group_urls.handlers + user_urls.handlers

    return handlers


def init_database(config):
    if config.redis_enabled:
        cache.init(host=config.redis_host, port=config.redis_port,
                   password=config.redis_password, pool_size=config.redis_pool_size,
                   socket_timeout=config.redis_timeout, db=config.redis_db)

        redis = cache.get_connection()
        redis.ping()

    mongoengine.connect(db="chat",
                        host=config.mongodb_connection_uri,
                        max_pool_size=config.mongodb_pool_size,
                        socketTimeoutMS=config.mongodb_timeout)
    print config.mongodb_connection_uri


def init_server(config):
    url_handlers = build_url_handlers()
    application = Application(
        handlers=url_handlers,
        config=config,
        debug=config.debug
    )
    application.add_handlers(config.host, url_handlers)

    http_server = httpserver.HTTPServer(application)
    http_server.listen(config.port_http)

    tcp_server = acceptor.Acceptor()
    tcp_server.listen(port=config.port_tcp)


def run_server(config):
    ioloop.IOLoop.instance().start()


def main():
    init_database(config=config)

    init_server(config=config)

    print "Chat server is started..."

    run_server(config=config)

    return 0


if __name__ == "__main__":
    # if len(sys.argv) == 2 and sys.argv[1] == "--daemon":
    #     daemon = daemonize.Daemonize(app="appspand.chat",
    #                                  pid="/tmp/appspand.chat.pid",
    #                                  action=main)
    #     daemon.start()
    # else:
        # Init signals handler for TERM and INT signals
        # (and so KeyboardInterrupt)
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)

        main()
