# Copyright (c) 2013 Appspand, Inc.

import json

import tornado.websocket

import message.controller
import room.controller
import user.controller
import net.websocket.controller

import net.protocols


MessageDispatcher = {
    "User_LoginReq": net.protocols.User_LoginReq,
    "Room_JoinReq": net.protocols.Room_JoinReq,
    "Room_LeaveReq": net.protocols.Room_LeaveReq,
    "Room_InviteReq": net.protocols.Room_InviteReq,
    "Message_SendReq": net.protocols.Message_SendReq,
    "Message_ReadReq": net.protocols.Message_ReadReq
}

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.user_uid = None

        print "websocket opened"
        # net.websocket.controller.add_user(user_uid='1', connection=self)

    def on_message(self, message):
        print "websocket:", message

        msg = json.loads(message)
        if "cmd" not in msg or "user_uid" not in msg or "payload" not in msg:
            raise AttributeError("Invalid command format")

        cmd = msg["cmd"]
        user_uid = msg["user_uid"]

        if cmd not in MessageDispatcher:
            raise KeyError("Unknown command name")

        cls = MessageDispatcher[cmd]
        req = net.protocols.from_json(cls=cls, raw_data=msg)

        if cmd == "User_LoginReq":
            self.user_login(user_uid=user_uid, request=req)
        elif cmd == "Room_JoinReq":
            self.room_join(user_uid=user_uid, request=req)
        elif cmd == "Room_LeaveReq":
            self.room_leave(user_uid=user_uid, request=req)
        elif cmd == "Room_InviteReq":
            self.room_invite(user_uid=user_uid, request=req)
        elif cmd == "Message_SendReq":
            self.message_send(user_uid=user_uid, request=req)
        elif cmd == "Message_ReadReq":
            self.message_read(user_uid=user_uid, request=req)
        else:
            #self.unknown_cmd(user_uid=user_uid, request=req)
            pass

    def on_close(self):
        print "websocket closed:", self.user_uid
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

    def room_join(self, user_uid, request):
        room_info = room.controller.join(room_uid=request.room_uid,
                                         user_uid=request.user_uid,
                                         invitee_uids=request.invitee_uids)
        if room_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot join room"

        ans = net.protocols.Room_JoinAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def room_leave(self, user_uid, request):
        room_info = room.controller.leave(room_uid=request.room_uid,
                                          user_uid=request.user_uid)
        if room_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot leave room"

        ans = net.protocols.Room_LeaveAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def room_invite(self, user_uid, request):
        room_info = room.controller.invite(room_uid=request.room_uid,
                                           user_uid=request.user_uid,
                                           invitee_uids=request.invitee_uids)
        if room_info is not None:
            error_code = 0
            error_message = "OK"
        else:
            error_code = 100
            error_message = "Cannot invite users"

        ans = net.protocols.Room_InviteAns()
        ans.request = request
        ans.error_code = error_code
        ans.error_message = error_message
        ans_json = net.protocols.to_json(user_uid=user_uid, message=ans)
        self.write_message(ans_json)

    def message_send(self, user_uid, request):
        message_info = message.controller.create(request.room_uid,
                                                 user_uid=request.user_uid,
                                                 message=request.message)
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
        message_info = message.controller.read(request.room_uid,
                                               user_uid=request.user_uid,
                                               message_uids=request.message_uids)
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
