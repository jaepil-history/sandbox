# Copyright (c) 2013 Appspand, Inc.

__all__ = ["Link"]


class Link(object):
    def __init__(self):
        super(Link, self).__init__()

        self.attributes = {}

    def hash(self):
        raise NotImplementedError("Link.hash() is not implemented")

    def close(self):
        raise NotImplementedError("Link.close() is not implemented")

    def send(self, message):
        raise NotImplementedError("Link.send() is not implemented")

    def ping(self, data):
        raise NotImplementedError("Link.ping() is not implemented")

    def set_attribute(self, key, value):
        self.attributes[key] = value

        return value

    def get_attribute(self, key):
        if key not in self.attributes:
            raise KeyError("key doesn't exists")

        return self.attributes[key]
