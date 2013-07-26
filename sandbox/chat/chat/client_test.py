#!/usr/bin/env python
#
# Copyright (c) 2013 Appspand, Inc.

import json
import sys
import socket

from tornado import gen
from tornado import httpclient
from tornado import ioloop
from tornado import websocket
from tornado import httputil
from tornado import iostream
from settings import base

import net.protocols


#config = base.parse_options()

base_host = "chat.appengine.local.appspand.com:8080"
# base_host = "chat.appengine.appspand.com:8080"
websocket_url = "ws://" + base_host + "/v1/ws"
base_api_url = "http://" + base_host + "/v1"


class WebSocketClient(object):
    def __init__(self):
        super(WebSocketClient, self).__init__()

    @gen.coroutine
    def connect(self, url):
        print "connect 1"
        self.connection = yield websocket.websocket_connect(url=url, connect_timeout=0.01)
        print "connect 2"

    @gen.coroutine
    def login(self, user_uid, user_name):
        print "login 1"
        login_req = net.protocols.User_LoginReq()
        login_req.user_uid = user_uid
        login_req.user_name = user_name
        login_req.seq = 1
        req = net.protocols.to_json(user_uid=user_uid, message=login_req)
        self.connection.write_message(req)

        res = yield self.connection.read_message()
        login_ans = net.protocols.User_LoginAns(json.loads(res))
        print login_ans.serialize()

        print "login 2"

    @gen.coroutine
    def sendTo(self, sender_uid, target_uid, message):
        print "starting to send a message"
        msg_req = net.protocols.Message_SendReq()
        msg_req.sender_uid = sender_uid
        msg_req.target_uid = target_uid
        msg_req.is_group = True
        msg_req.message = message
        req = net.protocols.to_json(user_uid=sender_uid, message=msg_req)
        self.connection.write_message(req)

        res = yield self.connection.read_message()
        msg_ans = net.protocols.Message_SendAns(json.loads(res))
        print msg_ans.serialize()

        print "finish to send a message"


@gen.coroutine
def run_websocket(url, user_uid, user_name):
    print "websocket:", url
    connection = yield websocket.websocket_connect(url=url)

    login_req = net.protocols.User_LoginReq()
    login_req.user_uid = user_uid
    login_req.user_name = user_name

    req = net.protocols.to_json(user_uid=user_uid, message=login_req)
    print req

    connection.write_message(req)

    while True:
        msg = yield connection.read_message()
        if msg is None:
            sys.exit(1)
        print msg


def run_tcpsocket(user_uid, user_name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    stream = iostream.IOStream(client)
    stream.connect(("chat.appengine.local.appspand.com", 20001))

    login_req = net.protocols.User_LoginReq()
    login_req.user_uid = user_uid
    login_req.user_name = user_name
    login_req.seq = 1

    req = net.protocols.to_json(user_uid=user_uid, message=login_req)
    req += "\r\n\r\n"
    print req

    stream.write(req)

    def on_received(data):
        print data

    stream.read_until_close(callback=lambda data: None, streaming_callback=on_received)


def user_login(user_uid, user_name):
    request_url = "%s/user?cmd=login&user_uid=%s&user_name=%s"\
                   % (base_api_url, user_uid, user_name)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def group_invite(group_uid, user_uid, invitee_uids):
    pass


def group_join(group_uid, user_uid):
    if group_uid is not None:
        request_url = "%s/group?cmd=join&group_uid=%s&user_uid=%s"\
                       % (base_api_url, group_uid, user_uid)
    else:
        request_url = "%s/group?cmd=join&user_uid=%s" \
                      % (base_api_url, user_uid)

    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def group_leave(group_uid, user_uid):
    request_url = "%s/group?cmd=leave&group_uid=%s&user_uid=%s" \
                  % (base_api_url, group_uid, user_uid)

    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def main():
    if len(sys.argv) < 3:
        print "client.py [User ID] [User Name] [Target ID]"
        return 1

    user_uid = sys.argv[1]
    user_name = sys.argv[2]
    target_uid = sys.argv[3]

    # client = WebSocketClient()
    # client.connect(url=websocket_url)
    # client.login(user_uid=user_uid, user_name=user_name)
    #run_tcpsocket(user_uid=user_uid, user_name=user_name)
    run_websocket(url=websocket_url, user_uid=user_uid, user_name=user_name)
    #websocket_connect(url=websocket_url)
    print "client started..."

    ioloop.IOLoop.instance().start()

    return 0


if __name__ == "__main__":
    main()
