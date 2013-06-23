# Copyright (c) 2013 Appspand, Inc.

import re

import tornado.escape
import tornado.gen
import tornado.web

import controller


class GroupHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        cmd = self.get_argument("cmd", None)
        if cmd is None:
            pass

        if cmd == "invite":
            self.group_invite()
        elif cmd == "join":
            self.group_join()
        elif cmd == "leave":
            self.group_leave()
        else:
            pass

        self.finish()

    def group_invite(self):
        group_uid = self.get_argument("group_uid")
        user_uid = self.get_argument("user_uid")
        invitees = self.get_argument("invitees")

        parsed_invitees = re.split(r"\s*[,]\s*", invitees.strip())

        invited_users = controller.invite(group_uid=group_uid,
                                          user_uid=user_uid,
                                          invitee_uids=parsed_invitees)

        self.write("%s" % invited_users.to_json())

    def group_join(self):
        group_uid = self.get_argument("group_uid", None)
        user_uid = self.get_argument("user_uid")
        invitees = self.get_argument("invitees", None)

        parsed_invitees = []
        if invitees is not None:
            parsed_invitees = re.split(r"\s*[,]\s*", invitees.strip())

        result = controller.join(group_uid=group_uid,
                                 user_uid=user_uid,
                                 invitee_uids=parsed_invitees)
        self.write("%s" % result.to_json())

    def group_leave(self):
        group_uid = self.get_argument("group_uid")
        user_uid = self.get_argument("user_uid")

        result = controller.leave(group_uid=group_uid, user_uid=user_uid)
        self.write("%s" % result.to_json())
