# Copyright (c) 2013 Appspand, Inc.

import json

from tornado.tcpserver import TCPServer

from log import logger
import message.controller
import group.controller

import net
import net.protocols
from net.tcp.link import TCPLink


class Acceptor(TCPServer):
    MessageDispatcher = {
        "User_LoginReq": net.protocols.User_LoginReq,
        "Group_JoinReq": net.protocols.Group_JoinReq,
        "Group_LeaveReq": net.protocols.Group_LeaveReq,
        "Group_InviteReq": net.protocols.Group_InviteReq,
        "Message_SendReq": net.protocols.Message_SendReq,
        "Message_ReadReq": net.protocols.Message_ReadReq,
        "Message_GetReq": net.protocols.Message_GetReq
    }

    streams = set()

    def __init__(self, *args, **kwargs):
        super(Acceptor, self).__init__(*args, **kwargs)

    def handle_stream(self, stream, address):
        link = TCPLink(stream=stream, address=address)
        link_id = link.hash()

        stream.link_id = link_id
        stream.set_close_callback(callback=lambda: self.on_closed(link))

        self.on_opened(link)

    def on_opened(self, link):
        link.user_uid = None

        logger.access.debug("Link(%d): on opened" % link.hash())

        net.LinkManager.instance().add(link_id=link.hash(), link=link)

        on_received = lambda data: self.on_received(link, data)
        # link.stream.read_until_close(callback=lambda data: None,
        #                              streaming_callback=on_received)
        link.stream.read_until(b"\r\n\r\n", callback=on_received)

    def on_received(self, link, data):
        logger.access.debug("Link(%d): on received - %s" % (link.hash(), data))
        #link.send(data)
        self.on_message(link, data)

        on_received = lambda data: self.on_received(link, data)
        link.stream.read_until(b"\r\n\r\n", callback=on_received)

    def on_closed(self, link):
        logger.access.debug("Link(%d): on closed" % link.hash())

        if link.user_uid:
            net.LinkManager.instance().logout(user_uid=link.user_uid)
        net.LinkManager.instance().remove(link_id=link.hash())

    def on_message(self, link, message):
        msg = json.loads(message)
        if "cmd" not in msg or "user_uid" not in msg or "payload" not in msg:
            raise AttributeError("Invalid command format")

        cmd = msg["cmd"]
        user_uid = msg["user_uid"]

        if cmd not in Acceptor.MessageDispatcher:
            raise KeyError("Unknown command name")

        cls = Acceptor.MessageDispatcher[cmd]
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
        elif cmd == "Message_ReadReq":
            self.message_read(link=link, user_uid=user_uid, request=req)
        elif cmd == "Message_GetReq":
            self.message_get(link=link, user_uid=user_uid, request=req)
        else:
            pass

    def user_login(self, link, user_uid, request):
        link.user_uid = request.user_uid

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
        ans_json = net.protocols.to_json(user_uid=link.user_uid, message=ans)
        link.send(ans_json)

    def user_logout(self, link, user_uid, request):
        pass

    def group_join(self, link, user_uid, request):
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
        link.send(ans_json)

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
        link.send(ans_json)

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
        link.send(ans_json)

    def message_send(self, link, user_uid, request):
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
        link.send(ans_json)

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
        link.send(ans_json)

    def message_get(self, link, user_uid, request):
        message_info = message.controller.get(src_uid=request.sender_uid,
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
        link.send(ans_json)
