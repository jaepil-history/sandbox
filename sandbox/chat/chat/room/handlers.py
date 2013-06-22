# Copyright (c) 2013 Appspand, Inc.

import re

import tornado.escape
import tornado.gen
import tornado.web

import controller


class RoomHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        cmd = self.get_argument("cmd", None)
        if cmd is None:
            pass

        if cmd == "invite":
            self.room_invite()
        elif cmd == "join":
            self.room_join()
        elif cmd == "leave":
            self.room_leave()
        else:
            pass

        self.finish()

    def room_invite(self):
        room_uid = self.get_argument("room_uid")
        user_uid = self.get_argument("user_uid")
        invitees = self.get_argument("invitees")

        parsed_invitees = re.split(r"\s*[,]\s*", invitees.strip())

        invited_users = controller.invite(room_uid=room_uid,
                                          user_uid=user_uid,
                                          invitee_uids=parsed_invitees)

        self.write("%s" % invited_users.to_json())

    def room_join(self):
        room_uid = self.get_argument("room_uid", None)
        user_uid = self.get_argument("user_uid")
        invitees = self.get_argument("invitees", None)

        parsed_invitees = []
        if invitees is not None:
            parsed_invitees = re.split(r"\s*[,]\s*", invitees.strip())

        result = controller.join(room_uid=room_uid,
                                 user_uid=user_uid,
                                 invitee_uids=parsed_invitees)
        self.write("%s" % result.to_json())

    def room_leave(self):
        room_uid = self.get_argument("room_uid")
        user_uid = self.get_argument("user_uid")

        result = controller.leave(room_uid=room_uid, user_uid=user_uid)
        self.write("%s" % result.to_json())
