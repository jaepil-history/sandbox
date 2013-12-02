# Copyright (c) 2013 Appspand, Inc.

import json

import tornado.websocket

from log import logger
import message.controller
import group.controller
import user.controller

import net
import net.protocols
from net.websocket.link import WebSocketLink


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    ProtocolMap = {
        "User_LoginReq": net.protocols.User_LoginReq,
        "User_UnregisterReq": net.protocols.User_UnregisterReq,
        "Group_JoinReq": net.protocols.Group_JoinReq,
        "Group_LeaveReq": net.protocols.Group_LeaveReq,
        "Group_InviteReq": net.protocols.Group_InviteReq,
        "Group_InfoReq": net.protocols.Group_InfoReq,
        "Message_GetSummary": net.protocols.Message_GetSummaryReq,
        "Message_SendReq": net.protocols.Message_SendReq,
        "Message_CancelReq": net.protocols.Message_CancelReq,
        "Message_OpenReq": net.protocols.Message_OpenReq,
        "Message_ReadReq": net.protocols.Message_ReadReq,
        "Message_GetReq": net.protocols.Message_GetReq,
        "Message_ClearReq": net.protocols.Message_ClearReq
    }
    MessageDispatcher = {}

    def __init__(self, *args, **kwargs):
        super(WebSocketHandler, self).__init__(*args, **kwargs)

        WebSocketHandler.MessageDispatcher = {
            "User_LoginReq": self.user_login,
            "User_UnregisterReq": self.user_unregister,
            "Group_JoinReq": self.group_join,
            "Group_LeaveReq": self.group_leave,
            "Group_InviteReq": self.group_invite,
            "Group_InfoReq": self.group_info,
            "Message_GetSummary": self.message_get_summary,
            "Message_SendReq": self.message_send,
            "Message_CancelReq": self.message_cancel,
            "Message_OpenReq": self.message_open,
            "Message_ReadReq": self.message_read,
            "Message_GetReq": self.message_get,
            "Message_ClearReq": self.message_clear
        }

    def open(self):
        self.user_uid = None

        link = WebSocketLink(self)
        self.link_id = link.hash()

        net.LinkManager.instance().add(link_id=link.hash(), link=link)

        logger.access.debug("WebSocket(%d): on opened" % self.link_id)

    def on_message(self, message):
        link = net.LinkManager.instance().find_one(link_id=self.link_id)
        if link is None:
            logger.access.debug("WebSocket(%d): link not found" % self.link_id)

        logger.access.debug("WebSocket(%d): on message - %s"
            % (self.link_id, message.encode("utf-8")))

        msg = json.loads(message)
        if "cmd" not in msg or "user_uid" not in msg or "payload" not in msg:
            raise AttributeError("Invalid command format")

        cmd = msg["cmd"]
        user_uid = msg["user_uid"]

        protocol_class =WebSocketHandler.ProtocolMap.get(cmd, None)
        if not protocol_class:
            raise KeyError("Unknown command name")

        req = net.protocols.from_json(cls=protocol_class, raw_data=msg)

        callback = WebSocketHandler.MessageDispatcher.get(cmd, None)
        if not callback:
            #self.unknown_cmd(link=link, user_uid=user_uid, request=req)
            raise KeyError("Unknown command name")

        callback(link=link, user_uid=user_uid, request=req)

    def on_close(self):
        logger.access.debug("WebSocket(%d): on closed" % self.link_id)

        if self.user_uid:
            net.LinkManager.instance().logout(user_uid=self.user_uid)
        net.LinkManager.instance().remove(link_id=self.link_id)

    def user_login(self, link, user_uid, request):
        self.user_uid = request.user_uid

        if net.LinkManager.instance().login(user_uid=user_uid, link=link):
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Connection is duplicated"

        user.controller.login(user_uid=user_uid, user_name=request.user_name)

        ans = net.protocols.User_LoginAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=self.user_uid, message=ans)
        self.write_message(ans_json)

    def user_logout(self, link, user_uid, request):
        pass

    def user_unregister(self, link, user_uid, request):
        self.user_uid = request.user_uid

        if net.LinkManager.instance().login(user_uid=user_uid, link=link):
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Connection is duplicated"

        user.controller.unregister(user_uid=user_uid)

        ans = net.protocols.User_UnregisterAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=self.user_uid, message=ans)
        self.write_message(ans_json)

    def group_join(self, link, user_uid, request):
        group_info = group.controller.join(group_uid=request.group_uid,
                                           user_uid=request.user_uid,
                                           invitee_uids=request.invitee_uids)
        if group_info is not None:
            error_code = 0
            error_message = "OK"
            if not request.group_uid:
                request.group_uid = group_info.uid
        else:
            error_code = 100
            error_message = "Cannot join group"

        member_info = user.controller.find(user_uids=request.invitee_uids)
        members = []
        for m in member_info:
            user_info = net.protocols.UserInfo()
            user_info.user_uid = m.uid
            user_info.user_name = m.name
            members.append(user_info)

        ans = net.protocols.Group_JoinAns()
        ans.request = request
        ans.invitees = members
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def group_leave(self, link, user_uid, request):
        error_code = 0
        error_message = "OK"

        try:
            message.controller.clear_all(user_uid=request.user_uid,
                                         target_uid=request.group_uid,
                                         is_group=True)
            group_info = group.controller.leave(group_uid=request.group_uid,
                                                user_uid=request.user_uid)
            if group_info is None:
                error_code = 100
                error_message = "Cannot leave group"
        except Exception as e:
            error_code = 200
            error_message = e.message
        finally:
            ans = net.protocols.Group_LeaveAns()
            ans.request = request
            ans.error_code = error_code
            ans.error_message = error_message
            ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
            self.write_message(ans_json)

    def group_invite(self, link, user_uid, request):
        group_info = group.controller.invite(group_uid=request.group_uid,
                                             user_uid=request.user_uid,
                                             invitee_uids=request.invitee_uids)
        if group_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot invite users"

        member_info = user.controller.find(user_uids=request.invitee_uids)
        members = []
        for m in member_info:
            user_info = net.protocols.UserInfo()
            user_info.user_uid = m.uid
            user_info.user_name = m.name
            members.append(user_info)

        ans = net.protocols.Group_InviteAns()
        ans.request = request
        ans.invitees = members
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def group_info(self, link, user_uid, request):
        group_info = group.controller.find(group_uid=request.group_uid)
        if group_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot invite users"

        # member_info = user.controller.find(user_uids=[user_uid for user_uid in group_info.members])
        member_info = user.controller.find(user_uids=group_info.members)
        members = []
        for m in member_info:
            user_info = net.protocols.UserInfo()
            user_info.user_uid = m.uid
            user_info.user_name = m.name
            members.append(user_info)

        ans = net.protocols.Group_InfoAns()
        ans.request = request
        ans.members = members
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_get_summary(self, link, user_uid, request):
        message_info = message.controller.get_summarized_info(src_uid=user_uid)

        error_code = 0
        error_message = "OK"

        summary = []
        for doc in message_info:
            mi = net.protocols.MessageInfo()
            mi.from_mongo_engine(doc)
            summary.append(mi)

        ans = net.protocols.Message_GetSummaryAns()
        ans.request = request
        ans.summary = summary
        ans.error_code = error_code
        ans.error_message = error_message

        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_send(self, link, user_uid, request):
        message_info = message.controller.send(sender_uid=request.sender_uid,
                                               target_uid=request.target_uid,
                                               message=request.message,
                                               is_secret=request.is_secret,
                                               is_group=request.is_group)

        mi = net.protocols.MessageInfo()

        if message_info is not None:
            mi.from_mongo_engine(message_info)
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot send a message"

        ans = net.protocols.Message_SendAns()
        ans.request = request
        ans.message_info = mi
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_cancel(self, link, user_uid, request):
        error_code = 0
        error_message = "OK"

        try:
            message_info = message.controller.cancel(sender_uid=request.sender_uid,
                                                     target_uid=request.target_uid,
                                                     message_uid=request.message_uid,
                                                     is_group=request.is_group)
            if message_info is None:
                error_code = 100
                error_message = "Cannot cancel message"
        except ValueError as e:
            error_code = 200
            error_message = e.message
        finally:
            ans = net.protocols.Message_CancelAns()
            ans.request = request
            ans.error_code = error_code
            ans.error_message = error_message
            ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
            self.write_message(ans_json)

    def message_open(self, link, user_uid, request):
        error_code = 0
        error_message = "OK"

        try:
            message_info = message.controller.open_secret_message(
                sender_uid=request.sender_uid,
                target_uid=request.target_uid,
                message_uid=request.message_uid,
                is_group=request.is_group)
            if message_info is None:
                error_code = 100
                error_message = "Cannot open message"
        except ValueError as e:
            error_code = 200
            error_message = e.message
        finally:
            ans = net.protocols.Message_OpenAns()
            ans.request = request
            ans.error_code = error_code
            ans.error_message = error_message
            ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
            self.write_message(ans_json)

    def message_read(self, link, user_uid, request):
        message_info = message.controller.read(user_uid=request.user_uid,
                                               target_uid=request.sender_uid,
                                               message_uids=request.message_uids,
                                               is_group=request.is_group)
        if message_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot read messages"

        messages = []
        for doc in message_info:
            mi = net.protocols.MessageInfo()
            mi.from_mongo_engine(doc)
            messages.append(mi)

        ans = net.protocols.Message_ReadAns()
        ans.request = request
        ans.message_info = messages
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_get(self, link, user_uid, request):
        message_info = message.controller.get(src_uid=request.user_uid,
                                              dest_uid=request.target_uid,
                                              since_uid=request.since_uid,
                                              count=request.count,
                                              message_uids=request.message_uids,
                                              is_group=request.is_group)
        if message_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot read messages"

        messages = []
        for doc in message_info:
            mi = net.protocols.MessageInfo()
            mi.from_mongo_engine(doc)
            messages.append(mi)

        ans = net.protocols.Message_GetAns()
        ans.request = request
        ans.message_info = messages
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_clear(self, link, user_uid, request):
        error_code = 0
        error_message = "OK"

        try:
            message.controller.clear_all(user_uid=request.user_uid,
                                         target_uid=request.target_uid,
                                         is_group=False)
        except KeyError as e:
            error_code = 100
            error_message = e.message
        finally:
            ans = net.protocols.Message_ClearAns()
            ans.request = request
            ans.error_code = error_code
            ans.error_message = error_message
            ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
            self.write_message(ans_json)
