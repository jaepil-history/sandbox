# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

import idgen
import protocol


def generate_unique_ids(app_id, count):
    status = 0
    message = "OK"
    unique_ids = []

    try:
        for i in range(0, count):
            unique_ids.append(idgen.get_next_id())
    except (SystemError, ValueError) as e:
    	status = 1
        message = e.message

    return protocol.UniqueIDs(app_id=app_id,
                              status=status, message=message,
                              unique_ids=unique_ids)
