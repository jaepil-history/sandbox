# Copyright (c) 2013 Appspand, Inc.

import tornado.escape

import net


class TCPLink(net.Link):
    def __init__(self, stream, address):
        super(TCPLink, self).__init__()

        self.stream = stream
        self.address = address

    def hash(self):
        return id(self.stream)

    def close(self):
        self.stream.close()

    def send(self, message):
        self.stream.write(tornado.escape.native_str(message))

    def ping(self, data):
        pass
