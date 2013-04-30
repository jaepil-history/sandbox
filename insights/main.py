#!/usr/bin/env python
#
# Copyright 2013 Appspand

import importlib

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import motor

import settings


cmd_options = tornado.options.OptionParser()
cmd_options.define(name="app", type=str, default="api", help="Application name")


class Application(tornado.web.Application):
    def __init__(self, handlers, options, mongodb_client):
        database = {
            "appspand": mongodb_client,
            "insights": mongodb_client
        }
        settings = {
            "debug": options.debug,
            "database": database,
            "options": options
        }

        super(Application, self).__init__(handlers, **settings)


def api_main(args, config):
    from insights.api import urls

    mongodb_client = motor.MotorClient(
        config.mongodb_connection_uri,
        max_concurrent=config.mongodb_max_concurrent,
        max_wait_time=config.mongodb_max_wait_time
    ).open_sync()

    application = Application(
        handlers=None,
        options=config,
        mongodb_client=mongodb_client
    )
    application.add_handlers("api.insights.appspand.com", urls.handlers)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(config.port)
    tornado.ioloop.IOLoop.instance().start()

    return 0


def cmd_main(args, config):
    if len(args) < 1:
        return 1

    app = importlib.import_module(".".join(["insights", "cmd", args[0]]))
    app.main(args, config)

    return 0


def main():
    args = cmd_options.parse_command_line()
    options = settings.parse_options()

    if cmd_options.app == "api":
        api_main(args, options)
    else:
        cmd_main(args, options)

    return 0


if __name__ == "__main__":
    main()
