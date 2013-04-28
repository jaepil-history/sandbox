from pymongo import MongoClient

from tornado.options import OptionParser

from ..api import models


options = OptionParser()
options.define(name="new", type=bool, default=False, help="Create new application")
options.define(name="delete", type=bool, default=False, help="Delete application")
options.define(name="list", type=bool, default=False, help="List all applications")


def create_application(config):
    db_client = MongoClient(host=config.mongodb_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_application = db_appspand.application

    name = raw_input("name: ")
    cluster_name = raw_input("cluster.name: ")
    cluster_db_name = raw_input("cluster.db_name: ")

    cluster = {
        "name": cluster_name,
        "db_name": cluster_db_name
    }
    ai = models.ApplicationInfo(name=name, cluster=cluster)
    doc = ai.to_python(validate=True)

    col_application.insert(doc)
    print doc


def delete_application(config):
    db_client = MongoClient(host=config.mongodb_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_application = db_appspand.application

    app_id = raw_input("Application ID: ")

    col_application.remove({"_id": app_id})


def list_application(config):
    db_client = MongoClient(host=config.mongodb_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_application = db_appspand.application

    for app in col_application.find():
        print app


def main(args, config):
    if len(args) < 2:
        options.print_help()
        return 1

    options.parse_command_line(args)
    if options.new is True:
        create_application(config)
    elif options.delete is True:
        delete_application(config)
    elif options.list is True:
        list_application(config)
    else:
        pass
