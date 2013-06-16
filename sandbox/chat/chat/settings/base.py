# Copyright (c) 2013 Appspand, Inc.

import os

from tornado import options


config_path = "settings.conf"


def parse_options(args=None):
    # Debugging
    options.define("debug", default=False, type=bool,
                   help="Turn on autoreload, log to stderr only")

    # Server Identity
    options.define("host", default="localhost", type=str, help="Server hostname")
    options.define("port", default=8888, type=int, help="Server port")

    # Celery
    options.define("celery_broker_url", type=str, help="URL for backend of Celery")
    options.define("celery_result_backend_url", type=str,
                   help="URL for backend of Celery to store result from tasks")
    options.define("celery_broker_max_connections", type=int, help="")

    # Redis
    options.define("redis_enabled", default=False, type=bool, help="Use redis server")
    options.define("redis_host", default="localhost", type=str, help="Redis server hostname")
    options.define("redis_port", default=6379, type=int, help="Redis server port")
    options.define("redis_password", default="", type=str, help="Redis server password")
    options.define("redis_pool_size", default=10, type=int, help="Max. concurrent connection")
    options.define("redis_timeout", default=1000 * 10, type=int,
                   help="Timeout to use for redis operations")
    options.define("redis_db", default=0, type=int, help="Redis database ID")

    # Database
    options.define("mongodb_connection_uri", default="mongodb://localhost:27017", type=str,
                   help="Connection URI for mongodb")
    options.define("mongodb_pool_size", default=10, type=int,
                   help="Max. concurrent connection")
    options.define("mongodb_timeout", default=1000 * 10, type=int,
                   help="Timeout to use for mongodb operations")

    # Session
    options.define("access_token_timeout_minutes", default=10, type=int,
                   help="Timeout to use for access_token expiration")

    # Parse config file, then command line, so command line switches take precedence
    if os.path.exists(config_path):
        print "Loading", config_path
        options.parse_config_file(config_path)
    else:
        print "No config file at", config_path

    if args is not None:
        options.parse_command_line(args)

    opts = options.options
    for required in ("host", "port", "mongodb_connection_uri"):
        if not opts.__getattr__(required):
            raise Exception("%s required" % required)

    return opts


def get_options():
    return options.options
