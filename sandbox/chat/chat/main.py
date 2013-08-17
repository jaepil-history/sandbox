#!/usr/bin/env python
#
# Copyright (c) 2013 Appspand, Inc.

import signal
import sys
import time

import mongoengine

from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado import web

import app.config
import interop.service
from log import logger
# from net.tcp import acceptor
from util import cache


def shutdown():
    io_loop = ioloop.IOLoop.instance()

    # io_loop.tcp_server.stop()

    # logging.info('Will shutdown in 2 seconds ...')
    interop.service.stop()
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
    logger.access_log.debug("mongodb connection url: %s"
                            % mongodb.connection_uri)


def init_server(config):
    url_handlers = build_url_handlers()
    application = Application(
        handlers=url_handlers,
        debug=config.debug,
        config=config
    )
    application.add_handlers(config.host, url_handlers)

    http_server = httpserver.HTTPServer(application)
    http_server.listen(config.port)

    # tcp_server = acceptor.Acceptor()
    # tcp_server.listen(port=config.port_tcp)


def init_service(config):
    if config.interop:
        interop.service.start()


def run_server(config):
    ioloop.IOLoop.instance().start()


def main():
    logger.init()

    if len(sys.argv) < 2:
        print "main.py [config]"
        return False

    options.parse_command_line()
    config = app.config.load_appcfg(sys.argv[1])

    init_database(config=config)

    init_server(config=config)
    init_service(config=config)

    logger.access_log.debug("Chat server is started...")

    run_server(config=config)

    return 0


if __name__ == "__main__":
    # Init signals handler for TERM and INT signals
    # (and so KeyboardInterrupt)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    main()
