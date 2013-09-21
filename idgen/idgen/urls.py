# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

import handlers


handlers = [
    (r"/v1/ids", handlers.UniqueIDHandler)
]
