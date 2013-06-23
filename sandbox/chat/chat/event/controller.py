# Copyright (c) 2013 Appspand, Inc.

import net.websocket.controller


def on_message_send(user_uid, member_uids, message):
    online, offline = net.websocket.controller.find(user_uids=member_uids)

    for uid, connection in online:
        connection.write_message(message)
    for uid in offline:
        # TODO: send message via push notification
        pass


def on_message_read(user_uid, member_uids, message_uids):
    pass


def on_input_started(group_uid, user_uid):
    pass


def on_input_stopped(group_uid, user_uid):
    pass


def on_user_invited(group_uid, user_uid, invitee_uids):
    pass


def on_user_kicked(group_uid, user_uid, target_user_uids):
    pass


def on_user_banned(group_uid, user_uid, target_user_uids):
    pass


def on_user_joined(group_uid, user_uid):
    pass


def on_user_leaved(group_uid, user_uid):
    pass
