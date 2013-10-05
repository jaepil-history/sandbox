# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Appspand, Inc.

import json
import yaml

import models


_appcfg = None


def load_appcfg(filename):
    global _appcfg
    with file(filename) as fp:
        opt = yaml.load(fp)
        _appcfg = models.AppConfig.from_json(json.dumps(opt))
    return _appcfg


def get_appcfg():
    global _appcfg
    return _appcfg


def is_production_stage():
    global _appcfg
    return _appcfg.application.stage == "production"
