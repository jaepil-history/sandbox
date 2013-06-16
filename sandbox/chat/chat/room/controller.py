# Copyright (c) 2013 Appspand, Inc.

# import hashlib

from util import cache
from util import idgen
from util import timestamp

import event.controller
import user.controller

import models


def create(owner_uid, invitee_uids, title=None):
    now = timestamp.get_timestamp()
    #uid = hashlib.sha1("%s-%d" % (owner_uid, now)).hexdigest()
    uid = ("%d" % idgen.get_next_id())

    members = [owner_uid] + invitee_uids
    room_info = models.Room(uid=uid,
                            title=title,
                            owner=owner_uid,
                            members=members,
                            dt_created=now)

    redis = cache.get_connection()
    key = ("room.%s" % uid)
    json = room_info.to_json()
    redis.set(name=key, value=json)

    event.controller.on_user_invited(room_uid=uid,
                                     user_uid=owner_uid,
                                     invitee_uids=invitee_uids)

    return room_info


def find(room_uid):
    redis = cache.get_connection()
    key = ("room.%s" % room_uid)
    json = redis.get(name=key)

    room_info = models.Room.from_json(json)

    return room_info


def invite(room_uid, user_uid, invitee_uids):
    room_info = find(room_uid=room_uid)
    if room_info is None:
        return None

    for uid in invitee_uids:
        if uid not in room_info.members:
            room_info.members.append(uid)

    redis = cache.get_connection()
    key = ("room.%s" % room_uid)
    json = room_info.to_json()
    redis.set(name=key, value=json)

    event.controller.on_user_invited(room_uid=room_uid,
                                     user_uid=user_uid,
                                     invitee_uids=invitee_uids)

    return room_info


def join(room_uid, user_uid):
    room_info = find(room_uid=room_uid)
    if room_info is None:
        return None

    if user_uid not in room_info.members:
        return None

    event.controller.on_user_joined(room_uid=room_uid,
                                    user_uid=user_uid)

    return room_info


def leave(room_uid, user_uid):
    room_info = find(room_uid=room_uid)
    if room_info is None:
        return None

    if user_uid not in room_info.members:
        return None

    room_info.members.remove(user_uid)

    redis = cache.get_connection()
    key = ("room.%s" % room_uid)
    json = room_info.to_json()
    redis.set(name=key, value=json)

    event.controller.on_user_leaved(room_uid=room_uid,
                                    user_uid=user_uid)

    return room_info
