# Copyright (c) 2013 Appspand, Inc.

current_id = 0


def get_next_id():
    global current_id
    current_id += 1
    return current_id
