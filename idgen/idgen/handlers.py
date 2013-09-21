# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

import tornado.gen
import tornado.web

from common.handlers import BaseHandler
import controller


class UniqueIDHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        app_id = int(self.get_argument("app_id"))
        count = int(self.get_argument("count"))

        unique_ids = controller.generate_unique_ids(app_id=app_id, count=count)

        self.write(unique_ids.to_json())
        self.finish()
