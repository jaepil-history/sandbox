# Copyright (c) 2013 Appspand, Inc.

from log import logger
from net.link_manager import LinkManager
import net.protocols

import interop.controller


def _send_message(sender_uid, target_uids, data):
    dest_uids = target_uids
    if sender_uid in target_uids:
        dest_uids.remove(sender_uid)

    (online, offline) = LinkManager.instance().find(user_uids=dest_uids)

    logger.access_log.debug("online: %d, offline: %d" % (len(online), len(offline)))

    for link in online:
        link.send(data)

    return offline


def on_message_send(sender_uid, group_uid, target_uids, message_info):
    mi = net.protocols.MessageInfo()
    mi.from_mongo_engine(message_info)

    noti = net.protocols.Message_NewNoti()
    noti.message_info = mi
    noti_str = net.protocols.to_json(user_uid=sender_uid, message=noti)

    offline_users = _send_message(sender_uid=sender_uid,
                                  target_uids=target_uids, data=noti_str)
    if offline_users:
        if group_uid is None:
            group_uid = 0
        interop.controller.push(sender_uid=sender_uid,
                                group_uid=group_uid,
                                target_uids=target_uids,
                                message_info=message_info)


def on_message_cancel(sender_uid, group_uid, target_uids, message_info):
    mi = net.protocols.MessageInfo()
    mi.from_mongo_engine(message_info)

    noti = net.protocols.Message_CancelNoti()
    noti.message_info = mi
    noti_str = net.protocols.to_json(user_uid=sender_uid, message=noti)

    offline_users = _send_message(sender_uid=sender_uid,
                                  target_uids=target_uids, data=noti_str)
    if offline_users:
        pass


def on_message_read(user_uid, group_uid, target_uids, messages):
    message_info = []
    for doc in messages:
        mi = net.protocols.MessageInfo()
        mi.from_mongo_engine(doc)
        message_info.append(mi)

    noti = net.protocols.Message_ReadNoti()
    noti.message_info = message_info
    noti_str = net.protocols.to_json(user_uid=user_uid, message=noti)

    offline_users = _send_message(sender_uid=user_uid,
                                  target_uids=target_uids, data=noti_str)
    if offline_users:
        pass


def on_input_started(group_uid, user_uid):
    pass


def on_input_stopped(group_uid, user_uid):
    pass


def on_user_invited(group_uid, user_uid, invitee_uids):
    noti = net.protocols.Group_InviteNoti()
    noti.group_uid = group_uid
    noti.user_uid = user_uid
    noti.invitee_uids = invitee_uids
    noti_str = net.protocols.to_json(user_uid=user_uid, message=noti)

    offline_users = _send_message(sender_uid=user_uid,
                                  target_uids=invitee_uids, data=noti_str)
    if offline_users:
        pass


def on_user_kicked(group_uid, user_uid, target_user_uids):
    pass


def on_user_banned(group_uid, user_uid, target_user_uids):
    pass


def on_user_joined(user_uid, group_uid, group_member_uids):
    pass


def on_user_leaved(user_uid, group_uid, target_uids):
    noti = net.protocols.Group_LeaveNoti()
    noti.group_uid = group_uid
    noti.user_uid = user_uid
    noti_str = net.protocols.to_json(user_uid=user_uid, message=noti)

    offline_users = _send_message(sender_uid=user_uid,
                                  target_uids=target_uids, data=noti_str)
    if offline_users:
        pass
