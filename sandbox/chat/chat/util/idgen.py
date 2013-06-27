# Copyright (c) 2013 Appspand, Inc.

# Reference
# http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram

import time


APPSPAND_ID_GEN_EPOCH = 1371894227468L

DATACENTER_ID_BITS = 5L
SHARD_ID_BITS = 5L
SEQUENCE_BITS = 12L

MAX_DATACENTER_ID = -1L ^ (-1L << DATACENTER_ID_BITS)
MAX_SHARD_ID = -1L ^ (-1L << SHARD_ID_BITS)
SEQUENCE_MASK = -1L ^ (-1L << SEQUENCE_BITS)

SHARD_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + SHARD_ID_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + SHARD_ID_BITS + DATACENTER_ID_BITS


class IDGenerator(object):
    _instance = None

    def __init__(self, datacenter_id, shard_id):
        super(IDGenerator, self).__init__()

        self.datacenter_id = datacenter_id
        self.shard_id = shard_id

        self.sequence = 0L
        self.last_timestamp = -1L

        self._sanity_check()

    @classmethod
    def instance(cls, **kwargs):
        if cls._instance is None:
            cls._instance = cls(**kwargs)

        return cls._instance

    def get_next_id(self):
        timestamp = self._get_timestamp()

        if timestamp < self.last_timestamp:
            raise SystemError("Clock moved backwards. "\
                              "Refusing to generate id for %d milliseconds"\
                              % (self.last_timestamp - timestamp))

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._get_next_timestamp(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - APPSPAND_ID_GEN_EPOCH) << TIMESTAMP_SHIFT)\
             | (self.datacenter_id << DATACENTER_ID_SHIFT)\
             | (self.shard_id << SHARD_ID_SHIFT)\
             | self.sequence
        return new_id

    def _get_timestamp(self):
        return int(round(time.time() * 1000))

    def _get_next_timestamp(self, last_timestamp):
        timestamp = int(round(time.time() * 1000))
        while timestamp <= last_timestamp:
            timestamp = self._get_timestamp()

        return timestamp

    def _sanity_check(self):
        if self.datacenter_id > MAX_DATACENTER_ID or self.datacenter_id < 0:
            raise ValueError("datancenter_id cannot be greater than %d or less than 0"
                             % MAX_DATACENTER_ID)

        if self.shard_id > MAX_SHARD_ID or self.shard_id < 0:
            raise ValueError("shard_id cannot be greater than %d or less than 0"
                             % MAX_SHARD_ID)


def get_next_id():
    return IDGenerator.instance(datacenter_id=1, shard_id=1).get_next_id()


def get_next_id_str():
    return str(get_next_id())
