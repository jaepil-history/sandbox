# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

import httplib
import urllib

import tornado.httpclient

import protocol


_APPSPAND_IDGEN_URL = "https://idgen.appspandapp.com"


def get_next_id(app_id, callback=None):
    pass


def get_next_ids(app_id, count, callback=None):
    def on_response(response):
        if response.code != httplib.OK:
            raise ValueError("IDGen service returns error. code: %d" % response.code)

        if len(response.body) == 0:
            raise ValueError("IDGen service returns empty result.")

        result = protocol.UniqueIDs.from_json(response.body)

        if callback:
            callback(result.unique_ids)

    args = {
        "app_id": app_id,
        "count": count,
        "v": 1
    }
    request_url = _APPSPAND_IDGEN_URL + "?" + urllib.urlencode(args)
    client = tornado.httpclient.AsyncHTTPClient()
    return client.fetch(request=request_url, callback=on_response)
