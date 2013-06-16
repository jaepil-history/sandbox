# Copyright (c) 2013 Appspand, Inc.

import handlers


handlers = [
    (r"/v1/message", handlers.MessageHandler)
]
