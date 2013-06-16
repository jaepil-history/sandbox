# Copyright (c) 2013 Appspand, Inc.

import re

import tornado.escape
import tornado.gen
import tornado.web

import controller


class MessageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        cmd = self.get_argument("cmd", None)
        if cmd is None:
            pass

        if cmd == "send":
            self.message_send()
        elif cmd == "read":
            self.message_read()
        else:
            pass

        self.finish()

    def message_send(self):
        room_uid = self.get_argument("room_uid")
        user_uid = self.get_argument("user_uid")
        message = self.get_argument("message", None)
        message = tornado.escape.url_unescape(message)

        message_info = controller.create(room_uid=room_uid,
                                         user_uid=user_uid,
                                         message=message)

        self.write("%s" % message_info.to_json())

    def message_read(self):
        room_uid = self.get_argument("room_uid")
        user_uid = self.get_argument("user_uid")
        message_uids = self.get_argument("message_uids", None)
        parsed_message_uids = re.split(r"\s*[,]\s*", message_uids.strip())

        message_info = controller.read(room_uid=room_uid,
                                       user_uid=user_uid,
                                       message_uids=parsed_message_uids)

        self.write("%s" % message_info.to_json())
