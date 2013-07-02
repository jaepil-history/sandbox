# Copyright (c) 2013 Appspand, Inc.

import json

import tornado.websocket

import message.controller
import group.controller
import user.controller
import net.websocket.controller

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
        "Message_ReadReq": net.protocols.Message_ReadReq,
        "Message_GetReq": net.protocols.Message_GetReq
    }

    def open(self):
        self.user_uid = None

        link = WebSocketLink(self)
        self.link_id = link.hash()

        net.LinkManager.instance().add(link_id=link.hash(), link=link)

        print "websocket opened:", self.link_id

    def on_message(self, message):
        link = net.LinkManager.instance().find(link_id=self.link_id)
        if link is None:
            print "link not found:", self.link_id

        print "websocket:", message

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
            self.user_login(user_uid=user_uid, request=req)
        elif cmd == "Group_JoinReq":
            self.group_join(user_uid=user_uid, request=req)
        elif cmd == "Group_LeaveReq":
            self.group_leave(user_uid=user_uid, request=req)
        elif cmd == "Group_InviteReq":
            self.group_invite(user_uid=user_uid, request=req)
        elif cmd == "Message_SendReq":
            self.message_send(user_uid=user_uid, request=req)
        elif cmd == "Message_ReadReq":
            self.message_read(user_uid=user_uid, request=req)
        elif cmd == "Message_GetReq":
            self.message_get(user_uid=user_uid, request=req)
        else:
            #self.unknown_cmd(user_uid=user_uid, request=req)
            pass

    def on_close(self):
        print "websocket closed:", self.link_id
        net.LinkManager.instance().remove(link_id=self.link_id)

        net.websocket.controller.remove_user(user_uid=self.user_uid, connection=self)

    def user_login(self, user_uid, request):
        self.user_uid = request.user_uid

        if net.websocket.controller.add_user(user_uid=self.user_uid, connection=self):
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

    def user_logout(self, user_uid, request):
        pass

    def group_join(self, user_uid, request):
        group_info = group.controller.join(group_uid=request.group_uid,
                                           user_uid=request.user_uid,
                                           invitee_uids=request.invitee_uids)
        if group_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot join group"

        ans = net.protocols.Group_JoinAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def group_leave(self, user_uid, request):
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

    def group_invite(self, user_uid, request):
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

    def message_send(self, user_uid, request):
        message_info = message.controller.send(sender_uid=request.sender_uid,
                                               target_uid=request.target_uid,
                                               message=request.message,
                                               is_group=request.is_group)
        if message_info is not None:
            message_uid = message_info.uid
            error_code = 0
            error_message = "OK"
        else:
            message_uid = 0
            error_code = 100
            error_message = "Cannot send a message"

        ans = net.protocols.Message_SendAns()
        ans.request = request
        ans.message_uid = message_uid
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_read(self, user_uid, request):
        message_info = message.controller.read(user_uid=request.user_uid,
                                               sender_uid=request.sender_uid,
                                               message_uids=request.message_uids,
                                               is_group=request.is_group)
        if message_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot read messages"

        ans = net.protocols.Message_ReadAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_get(self, user_uid, request):
        message_info = message.controller.get(src_uid=request.sender_uid,
                                              dest_uid=request.target_uid,
                                              since_uid=request.since_uid,
                                              count=request.count,
                                              is_group=request.is_group)
        if message_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot read messages"

        ans = net.protocols.Message_GetAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)
