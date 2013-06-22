# Copyright (c) 2013 Appspand, Inc.

from __future__ import absolute_import

import net


class WebsocketLink(net.Link):
    def __init__(self):
        super(WebsocketLink, self).__init__()

    def send(self, message):
        pass
