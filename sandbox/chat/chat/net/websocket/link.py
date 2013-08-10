# Copyright (c) 2013 Appspand, Inc.

import net


class WebSocketLink(net.Link):
    def __init__(self, connection):
        super(WebSocketLink, self).__init__()

        self.connection = connection

    def hash(self):
        return id(self.connection)

    def close(self):
        self.connection.close()

    def send(self, message):
        self.connection.write_message(message)

    def ping(self, data):
        self.connection.ping(data)
