#!/usr/bin/env python
#
# Copyright (c) 2013 Appspand, Inc.

import sys

from tornado import gen
from tornado import httpclient
from tornado import ioloop
from tornado import websocket
from tornado import httputil

from settings import base

import net.protocols


#config = base.parse_options()

base_host = "chat.appengine.local.appspand.com:8080"
websocket_url = "ws://" + base_host + "/v1/ws"
base_api_url = "http://" + base_host + "/v1"


@gen.coroutine
def run_websocket(url, user_uid, user_name):
    print "websocket:", url
    connection = yield websocket.websocket_connect(url=url, connect_timeout=0.01)

    login_req = net.protocols.User_LoginReq()
    login_req.user_uid = user_uid
    login_req.user_name = user_name
    login_req.seq = 1

    req = net.protocols.to_json(user_uid=user_uid, message=login_req)
    print req

    connection.write_message(req)

    while True:
        msg = yield connection.read_message()
        if msg is None:
            sys.exit(1)
        print msg


def user_login(user_uid, user_name):
    request_url = "%s/user?cmd=login&user_uid=%s&user_name=%s"\
                   % (base_api_url, user_uid, user_name)
    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def room_invite(room_uid, user_uid, invitee_uids):
    pass


def room_join(room_uid, user_uid):
    if room_uid is not None:
        request_url = "%s/room?cmd=join&room_uid=%s&user_uid=%s"\
                       % (base_api_url, room_uid, user_uid)
    else:
        request_url = "%s/room?cmd=join&user_uid=%s" \
                      % (base_api_url, user_uid)

    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def room_leave(room_uid, user_uid):
    request_url = "%s/room?cmd=leave&room_uid=%s&user_uid=%s" \
                  % (base_api_url, room_uid, user_uid)

    client = httpclient.HTTPClient()
    response = client.fetch(request=request_url,
                            connect_timeout=10.0,
                            request_timeout=10.0)
    print response.body
    client.close()


def main():
    if len(sys.argv) < 3:
        print "client.py [User ID] [User Name] [Room ID]"
        return 1

    user_uid = sys.argv[1]
    user_name = sys.argv[2]
    room_uid = None
    if len(sys.argv) > 3:
        room_uid = sys.argv[3]

    user_login(user_uid=user_uid, user_name=user_name)
    room_join(room_uid=room_uid, user_uid=user_uid)

    run_websocket(url=websocket_url, user_uid=user_uid, user_name=user_name)
    #websocket_connect(url=websocket_url)
    print "client started..."

    ioloop.IOLoop.instance().start()

    return 0


if __name__ == "__main__":
    main()
