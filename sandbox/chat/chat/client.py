#!/usr/bin/env python
#
# Copyright (c) 2013 Appspand, Inc.

from tornado import gen
from tornado import httpclient
from tornado import ioloop
from tornado import websocket

from settings import base


#config = base.parse_options()

base_host = "chat.appengine.local.appspand.com:8080"
websocket_url = "ws://" + base_host + "/v1/ws"
base_api_url = "http://" + base_host + "/v1"


@gen.coroutine
def run_websocket(url):
    print "websocket:", url
    connection = yield websocket.websocket_connect(url=url)

    print connection

    while True:
        msg = yield connection.read_message()
        print msg


def main():
    print "main:", websocket_url
    run_websocket(url=websocket_url)

    ioloop.IOLoop.instance().start()

    return 0


if __name__ == "__main__":
    main()
