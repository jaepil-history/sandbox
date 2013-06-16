# Copyright (c) 2013 Appspand, Inc.

from util import timestamp

import models


def create(user_uid, user_name, platform_id, device_token):
    devices = []
    if platform_id is not None and device_token is not None:
        devices.append(models.DeviceInfo(platform_id=platform_id,
                                         device_token=device_token))

    now = timestamp.get_timestamp()
    user_info = models.User(uid=user_uid,
                            name=user_name,
                            devices=devices,
                            dt_created=now,
                            dt_last_login=now)

    return user_info.save()


def find_one(user_uid):
    return models.User.objects(uid=user_uid).first()


def find(user_uids):
    result = models.User.objects(uid__in=user_uids)

    users = []
    if result is not None:
        for user in result:
            users.append(user)

    return users


def login(user_uid, user_name, platform_id, device_token):
    user_info = find_one(user_uid=user_uid)
    if user_info is None:
        user_info = create(user_uid=user_uid,
                           user_name=user_name,
                           platform_id=platform_id,
                           device_token=device_token)
    else:
        user_info.dt_last_login = timestamp.get_timestamp()
        user_info.save()

    return user_info


def logout(user_uid):
    pass
