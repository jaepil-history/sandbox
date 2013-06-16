# Copyright (c) 2013 Appspand, Inc.

connections = {}


def add_user(user_uid, connection):
    if connections.get(user_uid, None):
        return False

    connections[user_uid] = connection

    return True


def remove_user(user_uid, connection):
    if connections.get(user_uid, None) is None:
        return False

    del connections[user_uid]

    return True


def find_user(user_uid):
    return connections.get(user_uid, None)
