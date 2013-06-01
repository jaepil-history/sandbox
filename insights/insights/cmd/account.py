import getpass
import hashlib

from pymongo import MongoClient

from tornado.options import OptionParser

from insights.api import models


options = OptionParser()
options.define(name="new", type=bool, default=False, help="Create new account")
options.define(name="delete", type=bool, default=False, help="Delete account")
options.define(name="list", type=bool, default=False, help="List all accounts")


def create_account(config):
    db_client = MongoClient(host=config.mongodb_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_account = db_appspand.account

    name = raw_input("name: ")
    email = raw_input("email: ")
    password = getpass.getpass("password: ")

    ai = models.AccountInfo(name=name, email=email, password=hashlib.sha1(password).hexdigest())
    doc = ai.to_python(validate=True)

    col_account.insert(doc)
    print doc


def delete_account(config):
    db_client = MongoClient(host=config.mongodb_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)

    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_account = db_appspand.account

    email = raw_input("email: ")

    col_account.remove({"email": email})


def list_account(config):
    db_client = MongoClient(host=config.mongodb_connection_uri,
                            max_pool_size=config.mongodb_max_concurrent)
    db_appspand = db_client[config.mongodb_appspand_db_name]
    col_account = db_appspand.account

    for account in col_account.find():
        print account


def main(args, config):
    if len(args) < 2:
        options.print_help()
        return 1

    options.parse_command_line(args)
    if options.new is True:
        create_account(config)
    elif options.delete is True:
        delete_account(config)
    elif options.list is True:
        list_account(config)
    else:
        pass

