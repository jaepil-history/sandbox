#!/usr/bin/env python
#
# Copyright 2013 Appspand Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core
# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass


version = "1.0.0"
kwargs = {}


def readme():
    with open("README.md") as f:
        return f.read()


distutils.core.setup(
    name="Appspand AppEngine",
    version=version,
    author="Appspand Inc.",
    author_email="jaepil@appspand.com",
    url="http://www.appspand.com/",
    description="Appspand AppEngine is a distributed network application "\
                "framework for rapid development of scalable high-performance "\
                "backend services on top of the Appspand Cloud.",
    long_description=readme(),
    license="http://www.apache.org/licenses/LICENSE-2.0",
    platforms="any",
    packages=["appspand", "appspand.appengine", "appspand.appengine.amqp",
              "appspand.appengine.apns", "appspand.appengine.cacerts",
              "appspand.appengine.idgen", "appspand.appengine.insights",
              "appspand.appengine.keystone", "appspand.appengine.landscape",
              "appspand.appengine.probe", "appspand.appengine.trueskill"],
    package_data={
        "appspand.appengine.cacerts": ["ca-certificates.crt"]
        },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        ],
    **kwargs
)
