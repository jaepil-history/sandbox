# Copyright (c) 2013 Appspand, Inc.

from tornado.ioloop import PeriodicCallback


__all__ = ["LinkManager"]


class LinkManager(object):
    _instance = None

    def __init__(self):
        super(LinkManager, self).__init__()

        self.links = {}
        self._ping_timer = PeriodicCallback(callback=self._on_ping,
                                            callback_time=1000 * 60)
        self._ping_timer.start()

    def _on_ping(self):
        self.for_each(lambda link_id, link: link.ping(str(link_id)))

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
        for link_id, link in self.links.iteritems():
            f(link_id, link)
