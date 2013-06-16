# Copyright (c) 2013 Appspand, Inc.

import tornado.websocket

import ws.controller


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "websocket opened"
        ws.controller.add_user(user_uid='1', connection=self)

    def on_message(self, message):
        print "websocket:", message

    def on_close(self):
        print "websocket closed"
        ws.controller.remove_user(user_uid='1', connection=self)
