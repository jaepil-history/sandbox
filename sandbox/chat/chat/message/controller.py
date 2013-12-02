# Copyright (c) 2013 Appspand, Inc.

import datetime

import event.controller
import queue.controller
import group.controller

from util import idgen

import models


def _find_group(group_uid):
    group_info = group.controller.find(group_uid=group_uid)
    if group_info is None:
        raise ValueError("Invalid group id")

    return group_info


def find_one(message_uid):
    return models.Message.objects(uid=message_uid).first()


def find(message_uids):
    result = models.Message.objects(uid__in=message_uids)

    messages = []
    if result is not None:
        for m in result:
            messages.append(m)

    return messages


def send(sender_uid, target_uid, message, is_secret=False, is_group=False):
    group_uid = None
    if is_group:
        group_uid = target_uid
        group_info = _find_group(group_uid=target_uid)
        target_uids = group_info.members
        countdown = len(target_uids) - 1
    else:
        target_uids = [target_uid]
        countdown = 1

    now = datetime.datetime.utcnow()

    message_uid = idgen.get_next_id()
    issued_at = now
    expires_at = now + datetime.timedelta(days=7)
    recipient_count = countdown
    unveil_count = 0
    message_info = models.Message(uid=message_uid,
                                  sender_uid=sender_uid, group_uid=group_uid,
                                  message=message, countdown=countdown,
                                  issued_at=issued_at, expires_at=expires_at,
                                  is_secret=is_secret,
                                  recipient_count=recipient_count,
                                  unveil_count=unveil_count)
    message_info.save()

    for user_uid in target_uids:
        if sender_uid != user_uid:
            queue_info = queue.controller.find_one(user_uid=user_uid)
            if queue_info is None:
                queue_info = queue.controller.create(user_uid=user_uid)
            queue_info.message_uids.append(message_uid)
            queue_info.save()

    # if sender_uid not in target_uids:
    #     queue_info = queue.controller.find_one(user_uid=sender_uid)
    #     if queue_info is None:
    #         queue_info = queue.controller.create(user_uid=sender_uid)
    #     queue_info.message_uids.append(message_uid)
    #     queue_info.save()

    event.controller.on_message_send(sender_uid=sender_uid,
                                     group_uid=group_uid,
                                     target_uids=target_uids,
                                     message_info=message_info)

    return message_info


def cancel(sender_uid, target_uid, message_uid, is_group=False):
    group_uid = None
    if is_group:
        group_uid = target_uid
        group_info = _find_group(group_uid=target_uid)
        target_uids = group_info.members
    else:
        target_uids = [target_uid]

    message_info = find_one(message_uid=message_uid)
    if not message_info.is_secret:
        raise ValueError("Cannot cancel public message")
    if message_info.unveil_count > 0:
        raise ValueError("Cannot cancel unveiled message")

    for user_uid in target_uids:
        if sender_uid != user_uid:
            queue_info = queue.controller.find_one(user_uid=user_uid)
            if queue_info is None:
                continue
            if message_uid in queue_info.message_uids:
                queue_info.message_uids.remove(message_uid)
                queue_info.save()

    event.controller.on_message_cancel(sender_uid=sender_uid,
                                       group_uid=group_uid,
                                       target_uids=target_uids,
                                       message_info=message_info)

    return message_info


def open_secret_message(sender_uid, target_uid, message_uid, is_group=False):
    group_uid = 0
    if is_group:
        group_uid = target_uid

    message_info = find_one(message_uid=message_uid)
    if message_info is None:
        raise KeyError("Invalid message ID")

    if not message_info.is_secret:
        raise ValueError("Cannot open public message")

    message_info.unveil_count += 1
    if message_info.unveil_count < message_info.recipient_count:
        message_info.save()
    else:
        message_info.delete()

    event.controller.on_message_open(sender_uid=sender_uid,
                                     group_uid=group_uid,
                                     target_uid=message_info.sender_uid,
                                     message_uid=message_uid)

    return message_info


def clear_all(user_uid, target_uid, is_group=False):
    group_uid = 0
    if is_group:
        group_uid = target_uid
        # group_info = _find_group(group_uid=target_uid)
        # dest_uids = group_info.members
    else:
        # dest_uids = [target_uid]
        pass

    queue_info = queue.controller.find_one(user_uid=user_uid)
    if queue_info is None:
        raise KeyError("Unknown user ID")

    messages = find(queue_info.message_uids)
    for message_info in messages:
        if is_group:
            if group_uid != 0 and message_info.group_uid != group_uid:
                continue
        else:
            if target_uid != 0 and message_info.sender_uid != target_uid:
                continue

        message_info.countdown -= 1
        if message_info.countdown > 0:
            message_info.save()
        else:
            if message_info.is_secret and\
                message_info.unveil_count < message_info.recipient_count:
                message_info.save()
            else:
                message_info.delete()

        queue_info.message_uids.remove(message_info.uid)

    queue_info.save()

    # event.controller.on_message_read(user_uid=user_uid,
    #                                  group_uid=group_uid,
    #                                  target_uids=dest_uids,
    #                                  messages=messages)

    return True


def read(user_uid, target_uid, message_uids, is_group=False):
    group_uid = 0
    if is_group:
        group_uid = target_uid
        group_info = _find_group(group_uid=target_uid)
        dest_uids = group_info.members
    else:
        dest_uids = [target_uid]

    queue_info = queue.controller.find_one(user_uid=user_uid)
    if queue_info is None:
        queue_info = queue.controller.create(user_uid=user_uid)

    for message_uid in message_uids:
        if message_uid in queue_info.message_uids:
            queue_info.message_uids.remove(message_uid)

    queue_info.save()

    messages = find(message_uids=message_uids)
    for message_info in messages:
        message_info.countdown -= 1
        if message_info.countdown > 0:
            message_info.save()
        else:
            if message_info.is_secret and\
                message_info.unveil_count < message_info.recipient_count:
                message_info.save()
            else:
                message_info.delete()

    event.controller.on_message_read(user_uid=user_uid,
                                     group_uid=group_uid,
                                     target_uids=dest_uids,
                                     messages=messages)

    return messages


def flush_expired_messages(queue_info, messages):
    expired_uids = []
    for muid in queue_info.message_uids:
        found = False
        for mi in messages:
            if muid == mi.uid:
                found = True
                break
        if not found:
            expired_uids.append(muid)

    for muid in expired_uids:
        queue_info.message_uids.remove(muid)
    if expired_uids:
        queue_info.save()


def get(src_uid, dest_uid, since_uid=None, count=None, message_uids=None, is_group=False):
    queue_info = queue.controller.find_one(user_uid=src_uid)
    if queue_info is None:
        queue_info = queue.controller.create(user_uid=src_uid)

    messages = []
    if queue_info.message_uids:
        messages = find(message_uids=queue_info.message_uids)
    if message_uids:
        messages += find(message_uids=message_uids)

    flush_expired_messages(queue_info=queue_info, messages=messages)

    return messages


def get_messages(src_uid, dest_uid, since_uid, count, message_uids, reverse=True, is_group=False):
    queue_info = queue.controller.find_one(user_uid=src_uid)
    if queue_info is None:
        queue_info = queue.controller.create(user_uid=src_uid)

    target_message_uids = []
    if since_uid > 0:
        for muid in queue_info.message_uids:
            if reverse:
                if muid < since_uid:
                    continue
            else:
                if muid > since_uid:
                    continue

            if len(target_message_uids) < count:
                target_message_uids.append(muid)
            else:
                break

    for muid in message_uids:
        if muid not in target_message_uids:
            target_message_uids.append(muid)

    messages = find(message_uids=target_message_uids)

    flush_expired_messages(queue_info=queue_info, messages=messages)

    return messages


def get_summarized_info(src_uid):
    queue_info = queue.controller.find_one(user_uid=src_uid)
    if queue_info is None:
        queue_info = queue.controller.create(user_uid=src_uid)

    target_message_uids = []
    for muid in queue_info.message_uids:
        if reverse:
            if muid < since_uid:
                continue
        else:
            if muid > since_uid:
                continue

        if len(target_message_uids) < count:
            target_message_uids.append(muid)
        else:
            break

    messages = []
    if queue_info.message_uids:
        messages = find(message_uids=queue_info.message_uids)

    result = {}
    for m in reversed(messages):
        if m.group_uid not in result:
            result[m.group_uid] = m

    # flush_expired_messages(queue_info=queue_info, messages=messages)

    return messages
