#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#
# Copyright 2013 Appspand


from api import models

cluster = models.ClusterInfo(name='test', db_name='test')
app = models.ApplicationInfo(name='meteos', cluster=cluster)

cpu = models.UserInformation(uuid=1103, friends_count=100, country='Busan', birthday='1970/01/10', gender='u')

print app
print app.to_mongo()
print app.to_python()
print app.to_json()

print cpu
print cpu.to_mongo()
print cpu.to_python()
print cpu.to_json()