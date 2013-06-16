# Copyright (c) 2013 Appspand, Inc.

import ws.controller


def on_message_created(room_uid, user_uid, member_uids, message):
    c = ws.controller.find_user(user_uid=user_uid)
    if c is not None:
        c.write_message(message)


def on_message_read(room_uid, user_uid, member_uids, message_uids):
    pass


def on_input_started(room_uid, user_uid):
    pass


def on_input_stopped(room_uid, user_uid):
    pass


def on_user_invited(room_uid, user_uid, invitee_uids):
    pass


def on_user_kicked(room_uid, user_uid, target_user_uids):
    pass


def on_user_banned(room_uid, user_uid, target_user_uids):
    pass


def on_user_joined(room_uid, user_uid):
    pass


def on_user_leaved(room_uid, user_uid):
    pass
