# Copyright (c) 2013 Appspand, Inc.

import models
import event.controller
import room.controller

from util import idgen
from util import timestamp


def create(room_uid, user_uid, message):
    room_info = room.controller.find(room_uid=room_uid)
    if room_info is None:
        # TODO: error
        return None

    if user_uid not in room_info.members:
        # TODO: error
        return None

    # TODO: sets the value for attributes below
    uid = idgen.get_next_id()
    countdown = len(room_info.members) - 1
    issued_at = timestamp.get_timestamp()
    expires_at = 0
    message_info = models.Message(uid=uid, room_uid=room_uid, user_uid=user_uid,
                                  message=message, countdown=countdown,
                                  issued_at=issued_at, expires_at=expires_at)

    event.controller.on_message_created(room_uid=room_uid,
                                        user_uid=user_uid,
                                        member_uids=room_info.members,
                                        message=message)

    return message_info


def delete(room_uid, user_uid, message_uids):
    room_info = room.controller.find(room_uid=room_uid)
    if room_info is None:
        # TODO: error
        return None


def find_one(room_uid, user_uid, message_uid):
    room_info = room.controller.find(room_uid=room_uid)
    if room_info is None:
        # TODO: error
        return None


def find(room_uid, user_uid, message_uids):
    room_info = room.controller.find(room_uid=room_uid)
    if room_info is None:
        # TODO: error
        return None


def read(room_uid, user_uid, message_uids):
    room_info = room.controller.find(room_uid=room_uid)
    if room_info is None:
        # TODO: error
        return None

    if user_uid not in room_info.members:
        # TODO: error
        return None

    messages = find(room_uid=room_uid, user_uid=user_uid, message_uids=message_uids)
    for message_info in messages:
        if message_info.countdown > 0:
            message_info.countdown -= 1

    event.controller.on_message_read(room_uid=room_uid,
                                     user_uid=user_uid,
                                     member_uids=room_info.members,
                                     message_uids=message_uids)
