import os

from tornado import options


config_path = "insights/settings/settings.conf"


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
    options.define("mongodb_max_concurrent", default=10, type=int,
                   help="Max. concurrent connection")
    options.define("mongodb_max_wait_time", default=1000 * 10, type=int,
                   help="Max. concurrent connection")
    options.define("mongodb_appspand_db_name", default="appspand", type=str,
                   help="Database name for appspand applications")

    # Kontagent proxy
    options.define("enable_kontagent_proxy", default=False, type=bool,
                   help="Enable proxy to Kontagent API Server")
    options.define("kontagent_use_test_server", default=True, type=bool,
                   help="Enable to use Kontagent API Test Server")
    options.define("kontagent_app_id", type=str, help="Kontagent Application ID")

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
