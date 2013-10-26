# Copyright (c) 2013 Appspand, Inc.

# import hashlib
import datetime

from util import cache
from util import idgen

import app.config
import event.controller

import models


def _save(group_info):
    config = app.config.appcfg

    if config.database.redis.enabled:
        redis = cache.get_connection()
        key = ("group.%s" % group_info.uid)
        json = group_info.to_json()
        redis.set(name=key, value=json)
    else:
        group_info.save()

    return group_info


def _load(group_uid):
    config = app.config.appcfg

    group_info = None
    if config.database.redis.enabled:
        redis = cache.get_connection()
        key = ("group.%s" % group_uid)
        json = redis.get(name=key)
        if json is not None:
            group_info = models.Group.from_json(json)
    else:
        group_info = models.Group.objects(uid=group_uid).first()

    return group_info


def create(owner_uid, invitee_uids, title=None):
    now = datetime.datetime.utcnow()
    #uid = hashlib.sha1("%s-%d" % (owner_uid, now)).hexdigest()
    uid = ("%d" % idgen.get_next_id())

    members = [owner_uid] + invitee_uids
    group_info = models.Group(uid=uid,
                              title=title,
                              owner=owner_uid,
                              members=members,
                              created_at=now)

    _save(group_info=group_info)

    # event.controller.on_user_invited(group_uid=uid,
    #                                  user_uid=owner_uid,
    #                                  invitee_uids=invitee_uids)

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

    if not group_uid:
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

    event.controller.on_user_joined(user_uid=user_uid,
                                    group_uid=group_uid)

    return group_info


def leave(group_uid, user_uid):
    group_info = find(group_uid=group_uid)
    if group_info is None:
        return None

    if user_uid not in group_info.members:
        return None

    group_info.members.remove(user_uid)

    _save(group_info=group_info)

    event.controller.on_user_leaved(user_uid=user_uid,
                                    group_uid=group_uid,
                                    target_uids=group_info.members)

    return group_info
