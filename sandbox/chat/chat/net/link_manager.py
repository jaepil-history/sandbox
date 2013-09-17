# Copyright (c) 2013 Appspand, Inc.

from tornado.ioloop import PeriodicCallback


__all__ = ["LinkManager"]


class LinkManager(object):
    _instance = None

    def __init__(self):
        super(LinkManager, self).__init__()

        self.links = {}
        self.auth_links = {}
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

        return True

    def remove(self, link_id):
        del self.links[link_id]

        return True

    def login(self, user_uid, link):
        link.set_attribute("user_uid", user_uid)
        self.auth_links[user_uid] = link

        return True

    def logout(self, user_uid):
        del self.auth_links[user_uid]

        return True

    def find_one(self, link_id=None, user_uid=None):
        if link_id:
            return self.links.get(link_id, None)
        elif user_uid:
            return self.auth_links.get(user_uid, None)

        return None

    def find(self, link_ids=None, user_uids=None):
        online = []
        offline = []
        if link_ids:
            for link_id in link_ids:
                link = self.links.get(link_id, None)
                if link:
                    online.append(link)
                else:
                    offline.append(link_ids)
        elif user_uids:
            for user_uid in user_uids:
                link = self.auth_links.get(user_uid, None)
                if link:
                    online.append(link)
                else:
                    offline.append(user_uid)

        return online, offline

    def for_each(self, f):
        for link_id, link in self.links.iteritems():
            f(link_id, link)
