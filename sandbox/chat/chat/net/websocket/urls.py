# Copyright (c) 2013 Appspand, Inc.

import net.websocket.handlers


handlers = [
    (r"/v1/ws", net.websocket.handlers.WebSocketHandler)
]
