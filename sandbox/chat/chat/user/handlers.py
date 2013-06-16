# Copyright (c) 2013 Appspand, Inc.

import tornado.escape
import tornado.gen
import tornado.web

import controller


class UserHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        cmd = self.get_argument("cmd", None)
        if cmd is None:
            pass

        if cmd == "login":
            self.user_login()
        elif cmd == "logout":
            self.user_logout()
        else:
            pass

        self.finish()

    @tornado.web.asynchronous
    def post(self):
        pass

    def user_login(self):
        user_uid = self.get_argument("user_uid")
        user_name = self.get_argument("user_name")
        platform_id = self.get_argument("pid", None)
        device_token = self.get_argument("device_token", None)

        result = controller.login(user_uid=user_uid,
                                  user_name=user_name,
                                  platform_id=platform_id,
                                  device_token=device_token)
        self.write("%s" % result.to_json())

    def user_logout(self):
        pass
