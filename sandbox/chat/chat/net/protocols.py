# Copyright (c) 2013 Appspand, Inc.

import json

from schematics.models import Model
from schematics.types import IntType, LongType, StringType
from schematics.types.compound import ModelType, DictType, ListType


def to_json(user_uid, message):
    data = {
        "cmd": type(message).__name__,
        "user_uid": user_uid,
        "payload": message.serialize()
    }

    return json.dumps(data)


def from_json(cls, raw_data):
    if isinstance(raw_data, str):
        data = json.loads(raw_data)
    else:
        data = raw_data

    if "cmd" not in data or "user_uid" not in data or "payload" not in data:
        return None

    return cls(data["payload"])


class Message(Model):
    def to_json(self, role=None):
        data = self.serialize(role=role)
        return json.dumps(data)

    @classmethod
    def from_json(cls, data):
        obj = json.loads(data)
        return cls(obj)


# User
class User_DeviceInfo(Model):
    platform_id = IntType(required=True)
    device_token = StringType(required=True, max_length=512)


class User_LoginReq(Message):
    user_uid = StringType(required=True, max_length=512)
    user_name = StringType(required=True, max_length=512)
    profile_image_url = StringType(max_length=1024)
    devices = ListType(ModelType(User_DeviceInfo))


class User_LoginAns(Message):
    request = ModelType(User_LoginReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


# group
class group_JoinReq(Message):
    group_uid = StringType(max_length=512)
    user_uid = StringType(required=True, max_length=512)
    invitee_uids = ListType(StringType(max_length=512))


class group_JoinAns(Message):
    request = ModelType(group_JoinReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class group_LeaveReq(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)


class group_LeaveAns(Message):
    request = ModelType(group_LeaveReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class group_InviteReq(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)
    invitee_uids = ListType(StringType(max_length=512), required=True)


class group_InviteAns(Message):
    request = ModelType(group_InviteReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


# Message
class Message_NewNoti(Message):
    group_uid = StringType(required=True, max_length=512)
    sender_uid = StringType(required=True, max_length=512)
    message = StringType(required=True, max_length=1024)


class Message_SendReq(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)
    message = StringType(required=True, max_length=1024)


class Message_SendAns(Message):
    request = ModelType(Message_SendReq)
    message_uid = StringType(required=True, max_length=512)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Message_ReadReq(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)
    message_uids = ListType(StringType(max_length=512), required=True)


class Message_ReadAns(Message):
    request = ModelType(Message_ReadReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)
