# Copyright (c) 2013 Appspand, Inc.

import models
import event.controller
import queue.controller
import group.controller

from util import idgen
from util import timestamp


def _find_group(group_uid):
    group_info = group.controller.find(group_uid=group_uid)
    if group_info is None:
        raise ValueError("Invalid group id")

    return group_info


def send(src_uid, dest_uid, message, is_group=None):
    group_uid = None
    if is_group:
        group_uid = dest_uid
        group_info = _find_group(group_uid=dest_uid)
        dest_uids = group_info.members
        countdown = len(dest_uids) - 1
    else:
        dest_uids = [dest_uid]
        countdown = 1

    message_uid = idgen.get_next_id()
    issued_at = timestamp.get_timestamp()
    expires_at = 0
    message_info = models.Message(uid=message_uid,
                                  sender_uid=src_uid, group_uid=group_uid,
                                  message=message, countdown=countdown,
                                  issued_at=issued_at, expires_at=expires_at)
    message_info.save()

    for user_uid in dest_uids:
        queue_info = queue.controller.find_one(user_uid=user_uid)
        if queue_info is None:
            queue_info = queue.controller.create(user_uid=user_uid)
        queue_info.message_uids.append(message_uid)
        queue_info.save()

    if src_uid not in dest_uids:
        queue_info = queue.controller.find_one(user_uid=src_uid)
        if queue_info is None:
            queue_info = queue.controller.create(user_uid=src_uid)
        queue_info.message_uids.append(message_uid)
        queue_info.save()

    event.controller.on_message_send(user_uid=src_uid,
                                     member_uids=dest_uids,
                                     message=message_info)

    return message_info


def find_one(message_uid):
    return models.Message.objects(uid=message_uid).first()


def find(message_uids):
    result = models.Message.objects(uid__in=message_uids)

    messages = []
    if result is not None:
        for m in result:
            messages.append(m)

    return messages


def read(src_uid, dest_uid, message_uids, is_group=None):
    if is_group:
        group_info = _find_group(group_uid=dest_uid)
        dest_uids = group_info.members
    else:
        dest_uids = [dest_uid]

    queue_info = queue.controller.find_one(user_uid=src_uid)
    if queue_info is None:
        queue_info = queue.controller.create(user_uid=src_uid)

    for message_uid in message_uids:
        if message_uid in queue_info.message_uids:
            queue_info.message_uids.remove(message_uid)

    queue_info.save()

    messages = find(message_uids=message_uids)
    for message_info in messages:
        if message_info.countdown > 1:
            message_info.countdown -= 1
            message_info.save()
        else:
            message_info.delete()

    event.controller.on_message_read(user_uid=src_uid,
                                     member_uids=dest_uids,
                                     message_uids=message_uids)

    return messages


def get(src_uid, dest_uid, since_uid=None, count=None, is_group=False):
    queue_info = queue.controller.find_one(user_uid=src_uid)
    if queue_info is None:
        queue_info = queue.controller.create(user_uid=src_uid)

    return find(message_uids=queue_info.message_uids)
