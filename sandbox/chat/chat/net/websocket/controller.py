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


def find(user_uids):
    online_users = []
    offline_users = []

    for user_uid in user_uids:
        user = find_user(user_uid)
        if user is not None:
            online_users.append((user_uid, user))
        else:
            offline_users.append(user_uid)

    return online_users, offline_users
