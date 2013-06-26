# Copyright (c) 2013 Appspand, Inc.

import json

from tornado.tcpserver import TCPServer

import message.controller
import group.controller
import user.controller

import net
import net.protocols
import net.tcp.controller
from net.tcp.link import TCPLink


class Acceptor(TCPServer):
    MessageDispatcher = {
        "User_LoginReq": net.protocols.User_LoginReq,
        "group_JoinReq": net.protocols.group_JoinReq,
        "group_LeaveReq": net.protocols.group_LeaveReq,
        "group_InviteReq": net.protocols.group_InviteReq,
        "Message_SendReq": net.protocols.Message_SendReq,
        "Message_ReadReq": net.protocols.Message_ReadReq
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

        print "Link(%d): on opened" % link.hash()

        net.LinkManager.instance().add(link_id=link.hash(), link=link)

        on_received = lambda data: self.on_received(link, data)
        # link.stream.read_until_close(callback=lambda data: None,
        #                              streaming_callback=on_received)
        link.stream.read_until(b"\r\n\r\n", callback=on_received)

    def on_received(self, link, data):
        print "Link(%d): on received - %s" % (link.hash(), data)
        #link.send(data)
        self.on_message(link, data)

    def on_closed(self, link):
        net.LinkManager.instance().remove(link_id=link.hash())

        print "Link(%d): on closed" % link.hash()

        if link.user_uid:
            net.tcp.controller.remove_user(user_uid=link.user_uid, connection=link)

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
        elif cmd == "group_JoinReq":
            self.group_join(link=link, user_uid=user_uid, request=req)
        elif cmd == "group_LeaveReq":
            self.group_leave(link=link, user_uid=user_uid, request=req)
        elif cmd == "group_InviteReq":
            self.group_invite(link=link, user_uid=user_uid, request=req)
        elif cmd == "Message_SendReq":
            self.message_send(link=link, user_uid=user_uid, request=req)
        elif cmd == "Message_ReadReq":
            self.message_read(link=link, user_uid=user_uid, request=req)
        else:
            pass

    def user_login(self, link, user_uid, request):
        link.user_uid = request.user_uid

        if net.tcp.controller.add_user(user_uid=link.user_uid, connection=link):
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

        ans = net.protocols.group_JoinAns()
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

        ans = net.protocols.group_LeaveAns()
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

        ans = net.protocols.group_InviteAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        link.send(ans_json)

    def message_send(self, link, user_uid, request):
        message_info = message.controller.send(src_uid=request.user_uid,
                                               dest_uid=request.group_uid,
                                               message=request.message,
                                               is_group=True)
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
        message_info = message.controller.read(src_uid=request.user_uid,
                                               dest_uid=request.group_uid,
                                               message_uids=request.message_uids,
                                               is_group=True)
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
        link.send(ans_json)
