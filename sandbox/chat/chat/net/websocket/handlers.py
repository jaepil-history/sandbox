# Copyright (c) 2013 Appspand, Inc.

import json

import tornado.websocket

from log import logger
import message.controller
import group.controller

import net
import net.protocols
from net.websocket.link import WebSocketLink


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    MessageDispatcher = {
        "User_LoginReq": net.protocols.User_LoginReq,
        "Group_JoinReq": net.protocols.Group_JoinReq,
        "Group_LeaveReq": net.protocols.Group_LeaveReq,
        "Group_InviteReq": net.protocols.Group_InviteReq,
        "Message_SendReq": net.protocols.Message_SendReq,
        "Message_CancelReq": net.protocols.Message_CancelReq,
        "Message_ReadReq": net.protocols.Message_ReadReq,
        "Message_GetReq": net.protocols.Message_GetReq
    }

    def open(self):
        self.user_uid = None

        link = WebSocketLink(self)
        self.link_id = link.hash()

        net.LinkManager.instance().add(link_id=link.hash(), link=link)

        logger.access_log.debug("WebSocket(%d): on opened" % self.link_id)

    def on_message(self, message):
        link = net.LinkManager.instance().find_one(link_id=self.link_id)
        if link is None:
            logger.access_log.debug("WebSocket(%d): link not found" % self.link_id)

        logger.access_log.debug("WebSocket(%d): on message - %s" % (self.link_id, message.encode("utf-8")))

        msg = json.loads(message)
        if "cmd" not in msg or "user_uid" not in msg or "payload" not in msg:
            raise AttributeError("Invalid command format")

        cmd = msg["cmd"]
        user_uid = msg["user_uid"]

        if cmd not in WebSocketHandler.MessageDispatcher:
            raise KeyError("Unknown command name")

        cls = WebSocketHandler.MessageDispatcher[cmd]
        req = net.protocols.from_json(cls=cls, raw_data=msg)

        if cmd == "User_LoginReq":
            self.user_login(link=link, user_uid=user_uid, request=req)
        elif cmd == "Group_JoinReq":
            self.group_join(link=link, user_uid=user_uid, request=req)
        elif cmd == "Group_LeaveReq":
            self.group_leave(link=link, user_uid=user_uid, request=req)
        elif cmd == "Group_InviteReq":
            self.group_invite(link=link, user_uid=user_uid, request=req)
        elif cmd == "Message_SendReq":
            self.message_send(link=link, user_uid=user_uid, request=req)
        elif cmd == "Message_CancelReq":
            self.message_cancel(link=link, user_uid=user_uid, request=req)
        elif cmd == "Message_ReadReq":
            self.message_read(link=link, user_uid=user_uid, request=req)
        elif cmd == "Message_GetReq":
            self.message_get(link=link, user_uid=user_uid, request=req)
        else:
            #self.unknown_cmd(link=link, user_uid=user_uid, request=req)
            pass

    def on_close(self):
        logger.access_log.debug("WebSocket(%d): on closed" % self.link_id)

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

        ans = net.protocols.User_LoginAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=self.user_uid, message=ans)
        self.write_message(ans_json)

    def user_logout(self, link, user_uid, request):
        pass

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

        ans = net.protocols.Group_JoinAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def group_leave(self, link, user_uid, request):
        group_info = group.controller.leave(group_uid=request.group_uid,
                                            user_uid=request.user_uid)
        if group_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot leave group"

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

        ans = net.protocols.Group_InviteAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_send(self, link, user_uid, request):
        message_info = message.controller.send(sender_uid=request.sender_uid,
                                               target_uid=request.target_uid,
                                               message=request.message,
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
        message_info = message.controller.cancel(sender_uid=request.sender_uid,
                                                 target_uid=request.target_uid,
                                                 message_uid=request.message_uid,
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
