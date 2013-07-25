# Copyright (c) 2013 Appspand, Inc.

# import hashlib

from util import cache
from util import idgen
from util import timestamp

import event.controller
import user.controller
from settings import base

import models


config = base.get_options()


def _save(group_info):
    if config.redis_enabled:
        redis = cache.get_connection()
        key = ("group.%s" % group_info.uid)
        json = group_info.to_json()
        redis.set(name=key, value=json)
    else:
        group_info.save()

    return group_info


def _load(group_uid):
    group_info = None

    if config.redis_enabled:
        redis = cache.get_connection()
        key = ("group.%s" % group_uid)
        json = redis.get(name=key)
        if json is not None:
            group_info = models.Group.from_json(json)
    else:
        group_info = models.Group.objects(uid=group_uid).first()

    return group_info


def create(owner_uid, invitee_uids, title=None):
    now = timestamp.get_timestamp()
    #uid = hashlib.sha1("%s-%d" % (owner_uid, now)).hexdigest()
    uid = ("%d" % idgen.get_next_id())

    members = [owner_uid].append(invitee_uids)
    group_info = models.Group(uid=uid,
                              title=title,
                              owner=owner_uid,
                              members=members,
                              created_at=now)

    _save(group_info=group_info)

    event.controller.on_user_invited(group_uid=uid,
                                     user_uid=owner_uid,
                                     invitee_uids=invitee_uids)

    return group_info


def find(group_uid):
    return _load(group_uid=group_uid)


def invite(group_uid, user_uid, invitee_uids):
    if group_uid is None:
        group_info = create(owner_uid=user_uid, invitee_uids=invitee_uids)
    else:
        group_info = find(group_uid=group_uid)
        if group_info is None:
            return None

        for uid in invitee_uids:
            if uid not in group_info.members:
                group_info.members.append(uid)

    _save(group_info=group_info)

    event.controller.on_user_invited(group_uid=group_uid,
                                     user_uid=user_uid,
                                     invitee_uids=invitee_uids)

    return group_info


def join(group_uid, user_uid, invitee_uids):
    # group_info = find(group_uid=group_uid)
    # if group_info is None:
    #     return None
    #
    # if user_uid not in group_info.members:
    #     return None

    if group_uid is None:
        group_info = create(owner_uid=user_uid, invitee_uids=invitee_uids)
    else:
        group_info = find(group_uid=group_uid)
        if group_info is None:
            return None

        if user_uid not in group_info.members:
            group_info.members.append(user_uid)
        # for uid in invitee_uids:
        #     if uid not in group_info.members:
        #         group_info.members.append(uid)

    _save(group_info=group_info)

    event.controller.on_user_joined(group_uid=group_uid,
                                    user_uid=user_uid)

    return group_info


def leave(group_uid, user_uid):
    group_info = find(group_uid=group_uid)
    if group_info is None:
        return None

    if user_uid not in group_info.members:
        return None

    group_info.members.remove(user_uid)

    _save(group_info=group_info)

    event.controller.on_user_leaved(group_uid=group_uid,
                                    user_uid=user_uid)

    return group_info
