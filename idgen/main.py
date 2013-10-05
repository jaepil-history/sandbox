#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

import sys

from tornado import httpserver
from tornado import ioloop
from tornado import options
from tornado import process
from tornado import web

from config import loader
# from common import cache
from log import logger


class Application(web.Application):
    pass


def build_url_handlers():
    from idgen import urls as idgen_urls

    handlers = idgen_urls.handlers

    return handlers


# def init_services(config):
#     if config.application.stage == "local":
#         return

#     import newrelic.agent
#     newrelic.agent.initialize("../conf/newrelic.ini",
#                               config.application.stage)
#     newrelic.agent.register_application()


# def init_database(config):
#     database = config.database

#     redis = database.redis
#     if redis.enabled:
#         cache.init(host=redis.host, port=redis.port,
#                    password=redis.password, pool_size=redis.connection_pool,
#                    socket_timeout=redis.timeout, db=redis.db)

#         r = cache.get_connection()
#         r.ping()

#     for mongodb in database.mongodb:
#         mongoengine.connect(db="meteos",
#                             alias=mongodb.alias,
#                             host=mongodb.connection_uri,
#                             max_pool_size=mongodb.connection_pool,
#                             socketTimeoutMS=mongodb.timeout)


def init_http_server(config, port):
    url_handlers = build_url_handlers()
    application = Application(
        handlers=None,
        debug=config.debug,
        config=config
    )
    for host_name in config.server.hosts:
        application.add_handlers(host_name.host, url_handlers)

    ssl_options = None
    if config.security.ssl_cert and config.security.ssl_key:
        ssl_options = {
            "certfile": config.security.ssl_cert,
            "keyfile": config.security.ssl_key,
        }

    http_server = httpserver.HTTPServer(application, ssl_options=ssl_options)
    http_server.listen(port)


def run_server(config):
    ioloop.IOLoop.instance().start()


def main():
    if len(sys.argv) < 2:
        print "main.py [config]"
        return False

    options.parse_command_line()
    config = loader.load_appcfg(sys.argv[1])
    task_id = 0
    if len(sys.argv) > 2:
        task_id = int(sys.argv[2])

    listen_port = config.server.base_port + task_id

    logger.init(config=config, task_id=task_id)
    logger.general.debug("Configuration dump: %s" % config.to_json())

    # init_services(config=config)
    # init_database(config=config)
    init_http_server(config=config, port=listen_port)

    # test(config=config)
    # for idx in range(1, 100):
    #     create_test_user(idx=idx)

    logger.general.debug("IDGen server is started in %s mode..." % config.application.stage)
    logger.general.debug("Total processes: %d" % config.server.num_processes)
    logger.general.debug("Task ID: %d" % task_id)
    logger.general.debug("HTTP listen port: %d" % listen_port)

    run_server(config=config)

    return True


if __name__ == "__main__":
    main()
