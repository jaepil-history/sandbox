#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand

import os

from tornado import options


config_path = "settings.conf"


def parse_options(args=None):
    # Debugging
    options.define("debug", default=False, type=bool,
                   help="Turn on autoreload, log to stderr only")

    # Startup
    options.define("ensure_indexes", default=False, type=bool,
                   help="Ensure collection indexes before starting")
    options.define("rebuild_indexes", default=False, type=bool,
                   help="Drop all indexes and recreate before starting")
    options.define("logpath", type=str, default="log",
                   help="Location of logging (if debug mode is off)")

    # Server Identity
    options.define("host", default="localhost", type=str, help="Server hostname")
    options.define("port", default=8888, type=int, help="Server port")

    # Database
    options.define("mongodb_connection_uri", default="mongodb://localhost:27017", type=str,
                   help="Connection URI for mongodb")
    options.define("mongodb_appspand_connection_uri", default="mongodb://localhost:27017", type=str,
                   help="Appspand Connection URI for mongodb")
    options.define("mongodb_insights_connection_uri", default="mongodb://localhost:27017", type=str,
                   help="Insights Connection URI for mongodb")
    options.define("mongodb_processed_connection_uri", default="mongodb://localhost:27017", type=str,
                   help="Processed Connection URI for mongodb")
    options.define("mongodb_pool_size", default=10, type=int,
                   help="Max. concurrent connection")
    options.define("mongodb_timeout", default=1000 * 10, type=int,
                   help="Timeout to use for mongodb operations")
    options.define("mongodb_appspand_db_name", default="appspand", type=str,
                   help="Database name for appspand applications")
    options.define("mongodb_insights_db_name", default="insights", type=str,
                   help="Database name for insights data")
    options.define("mongodb_processed_db_name", default="processed", type=str,
                   help="Database name for processed data")

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
