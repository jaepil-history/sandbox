# Copyright (c) 2013 Appspand, Inc.

import net.websocket.controller


def on_message_send(room_uid, user_uid, member_uids, message):
    online, offline = net.websocket.controller.find(user_uids=member_uids)

    for uid, connection in online:
        connection.write_message(message)
    for uid in offline:
        # TODO: send message via push notification
        pass


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
