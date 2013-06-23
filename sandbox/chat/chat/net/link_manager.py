# Copyright (c) 2013 Appspand, Inc.

__all__ = ["LinkManager"]


class LinkManager(object):
    _instance = None

    def __init__(self):
        super(LinkManager, self).__init__()

        self.links = {}

    @classmethod
    def instance(cls, **kwargs):
        if cls._instance is None:
            cls._instance = cls(**kwargs)

        return cls._instance

    def add(self, link_id, link):
        self.links[link_id] = link

    def remove(self, link_id):
        del self.links[link_id]

    def find(self, link_id):
        return self.links.get(link_id, None)

    def for_each(self, f):
        for link_id, link in self.links:
            f(link_id, link)
