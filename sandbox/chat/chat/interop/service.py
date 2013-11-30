# Copyright (c) 2013 Appspand, Inc.

import json

from threading import Thread

from tornado.ioloop import IOLoop

from log import logger
import message.controller
import net.protocols

import controller


class QueuePoller(Thread):
    def __init__(self):
        super(QueuePoller, self).__init__()

        self.terminated = False

    def start(self):
        super(QueuePoller, self).start()

    def stop(self):
        self.terminated = True

    def run(self):
        while not self.terminated:
            logger.access.debug("checking messages from snek queue...")
            items = controller.pull()
            if items:
                IOLoop.instance().add_callback(self.on_items, items)

    def on_items(self, items):
        for item in items:
            item_data = json.loads(item)
            logger.access.debug("pull from snek: %r" % item_data)

            send_req = net.protocols.Message_SendReq(item_data)
            message.controller.send(sender_uid=send_req.sender_uid,
                                    target_uid=send_req.target_uid,
                                    message=send_req.message,
                                    is_group=send_req.is_group)


_started = False
_queue_poller = QueuePoller()


def start():
    global _started
    global _queue_poller

    if _started:
        return

    _queue_poller.start()
    _started = True


def stop():
    global _started
    global _queue_poller

    if _started:
        _started = False
        _queue_poller.stop()
        _queue_poller.join()
