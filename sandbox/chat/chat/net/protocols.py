# Copyright (c) 2013 Appspand, Inc.

import json

from schematics.models import Model
# from schematics.exceptions import ConversionError
from schematics.types import BaseType, BooleanType, IntType, LongType, StringType
from schematics.types.compound import ModelType, DictType, ListType

from util import timestamp

# from mongoengine import Document
# from mongoengine import EmbeddedDocument
#
# import message.models


# class MongoEngineDocumentType(BaseType):
#     def __init__(self, document_type, **kwargs):
#         self.document_type = document_type
#
#         super(MongoEngineDocumentType, self).__init__(**kwargs)
#
#     def convert(self, value):
#         if not isinstance(value, (Document, EmbeddedDocument)):
#             raise ConversionError(u'Must be subclass of BaseDocument.')
#
#         return value.to_json()
#
#     def to_primitive(self, value):
#         return value.to_json()


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
class UserInfo(Message):
    user_uid = StringType(required=True, max_length=512)
    user_name = StringType(required=True, max_length=512)


class User_LoginReq(Message):
    user_uid = StringType(required=True, max_length=512)
    user_name = StringType(required=True, max_length=512)


class User_LoginAns(Message):
    request = ModelType(User_LoginReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class User_UnregisterReq(Message):
    user_uid = StringType(required=True, max_length=512)


class User_UnregisterAns(Message):
    request = ModelType(User_UnregisterReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


# Group
class Group_JoinReq(Message):
    group_uid = StringType(max_length=512)
    user_uid = StringType(required=True, max_length=512)
    invitee_uids = ListType(StringType(max_length=512))


class Group_JoinAns(Message):
    request = ModelType(Group_JoinReq)
    invitees = ListType(ModelType(UserInfo))
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Group_JoinNoti(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)


class Group_LeaveReq(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)


class Group_LeaveAns(Message):
    request = ModelType(Group_LeaveReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Group_LeaveNoti(Message):
    group_uid = StringType(required=True, max_length=512)
    user_info = ModelType(UserInfo, required=True)


class Group_InviteReq(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)
    invitee_uids = ListType(StringType(max_length=512), required=True)


class Group_InviteAns(Message):
    request = ModelType(Group_InviteReq)
    invitees = ListType(ModelType(UserInfo))
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Group_InviteNoti(Message):
    group_uid = StringType(required=True, max_length=512)
    user_uid = StringType(required=True, max_length=512)
    invitees = ListType(ModelType(UserInfo))


class Group_InfoReq(Message):
    group_uid = StringType(max_length=512)
    user_uid = StringType(required=True, max_length=512)


class Group_InfoAns(Message):
    request = ModelType(Group_InviteReq)
    members = ListType(ModelType(UserInfo))
    error_code = IntType(required=True)
    error_message = StringType(required=True)


# Message
class MessageInfo(Message):
    uid = LongType(required=True)
    sender_uid = StringType(required=True, max_length=512)
    group_uid = StringType(max_length=512)
    message = StringType(required=True, max_length=10240)
    countdown = IntType(required=True)
    issued_at = IntType(required=True)
    expires_at = IntType(required=True)
    is_secret = BooleanType(default=False)
    recipient_count = IntType(default=0)
    unveil_count = IntType(default=0)

    def from_mongo_engine(self, document):
        self.uid = document.uid
        self.sender_uid = document.sender_uid
        self.group_uid = document.group_uid
        self.message = document.message
        self.countdown = document.countdown
        self.issued_at = timestamp.get_timestamp(document.issued_at)
        self.expires_at = timestamp.get_timestamp(document.expires_at)
        self.is_secret = document.is_secret
        self.recipient_count = document.recipient_count
        self.unveil_count = document.unveil_count

    def to_mongo_engine(self, document):
        document.uid = self.uid
        document.sender_uid = self.sender_uid
        document.group_uid = self.group_uid
        document.message = self.message
        document.countdown = self.countdown
        document.issued_at = timestamp.get_datetime(self.issued_at)
        document.expires_at = timestamp.get_datetime(self.expires_at)
        document.is_secret = self.is_secret
        document.recipient_count = self.recipient_count
        document.unveil_count = self.unveil_count


class Message_GetSummaryReq(Message):
    user_uid = StringType(required=True, max_length=512)


class Message_GetSummaryAns(Message):
    request = ModelType(Message_GetSummaryReq)
    summary = ListType(ModelType(MessageInfo))
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Message_SendReq(Message):
    sender_uid = StringType(required=True, max_length=512)
    target_uid = StringType(required=True, max_length=512)
    is_group = BooleanType(required=True)
    message = StringType(required=True, max_length=10240)
    is_secret = BooleanType(default=False)


class Message_SendAns(Message):
    request = ModelType(Message_SendReq)
    message_info = ModelType(MessageInfo, required=True)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Message_NewNoti(Message):
    message_info = ModelType(MessageInfo, required=True)


class Message_CancelReq(Message):
    sender_uid = StringType(required=True, max_length=512)
    target_uid = StringType(required=True, max_length=512)
    is_group = BooleanType(required=True)
    message_uid = LongType(required=True)


class Message_CancelAns(Message):
    request = ModelType(Message_CancelReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Message_CancelNoti(Message):
    message_info = ModelType(MessageInfo, required=True)


class Message_OpenReq(Message):
    sender_uid = StringType(required=True, max_length=512)
    target_uid = StringType(required=True, max_length=512)
    is_group = BooleanType(required=True)
    message_uid = LongType(required=True)


class Message_OpenAns(Message):
    request = ModelType(Message_CancelReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Message_OpenNoti(Message):
    sender_uid = StringType(required=True, max_length=512)
    target_uid = StringType(required=True, max_length=512)
    is_group = BooleanType(required=True)
    message_uid = LongType(required=True)


class Message_ReadReq(Message):
    user_uid = StringType(required=True, max_length=512)
    sender_uid = StringType(required=True, max_length=512)
    is_group = BooleanType(required=True)
    message_uids = ListType(LongType(), required=True)


class Message_ReadAns(Message):
    request = ModelType(Message_ReadReq)
    message_info = ListType(ModelType(MessageInfo))
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Message_ReadNoti(Message):
    message_info = ListType(ModelType(MessageInfo), required=True)


class Message_GetReq(Message):
    user_uid = StringType(required=True, max_length=512)
    target_uid = StringType(required=True, max_length=512)
    is_group = BooleanType(required=True)
    since_uid = LongType()
    count = IntType()
    message_uids = ListType(LongType())


class Message_GetAns(Message):
    request = ModelType(Message_GetReq)
    message_info = ListType(ModelType(MessageInfo))
    error_code = IntType(required=True)
    error_message = StringType(required=True)


class Message_ClearReq(Message):
    user_uid = StringType(required=True, max_length=512)
    target_uid = StringType(required=True, max_length=512)


class Message_ClearAns(Message):
    request = ModelType(Message_GetReq)
    error_code = IntType(required=True)
    error_message = StringType(required=True)
