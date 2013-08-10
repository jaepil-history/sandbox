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
        elif cmd == "get":
            self.message_get()
        else:
            pass

        self.finish()

    def message_send(self):
        user_uid = self.get_argument("user_uid")
        group_uid = self.get_argument("group_uid", None)
        dest_uid = self.get_argument("dest_uid", None)
        message = self.get_argument("message")
        message = tornado.escape.url_unescape(message)

        if group_uid is None and dest_uid is None:
            # TODO: Bad request
            raise KeyError("Invalid parameter")

        is_group = False
        if group_uid is not None:
            dest_uid = group_uid
            is_group = True

        message_info = controller.send(sender_uid=user_uid,
                                       target_uid=dest_uid,
                                       message=message,
                                       is_group=is_group)

        self.write("%s" % message_info.to_json())

    def message_read(self):
        user_uid = self.get_argument("user_uid")
        group_uid = self.get_argument("group_uid", None)
        dest_uid = self.get_argument("dest_uid", None)
        message_uids = self.get_argument("message_uids")
        parsed_message_uids = re.split(r"\s*[,]\s*", message_uids.strip())

        if group_uid is None and dest_uid is None:
            # TODO: Bad request
            raise KeyError("Invalid parameter")

        is_group = False
        if group_uid is not None:
            dest_uid = group_uid
            is_group = True

        message_infos = controller.read(user_uid=user_uid,
                                        target_uid=dest_uid,
                                        message_uids=parsed_message_uids,
                                        is_group=is_group)

        self.write("{\"messages\": [")
        self.write(", ".join(m.to_json() for m in message_infos))
        self.write("]}")

    def message_get(self):
        user_uid = self.get_argument("user_uid")
        group_uid = self.get_argument("group_uid", None)
        dest_uid = self.get_argument("dest_uid", None)
        since_uid = self.get_argument("since_uid", None)
        count = self.get_argument("count", None)

        if group_uid is None and dest_uid is None:
            # TODO: Bad request
            raise KeyError("Invalid parameter")

        is_group = False
        if group_uid is not None:
            dest_uid = group_uid
            is_group = True

        message_infos = controller.get(src_uid=user_uid,
                                       dest_uid=dest_uid,
                                       since_uid=since_uid,
                                       count=count,
                                       is_group=is_group)

        self.write("{\"messages\": [")
        self.write(", ".join(m.to_json() for m in message_infos))
        self.write("]}")
