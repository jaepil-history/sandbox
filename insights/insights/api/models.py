import json
import time
import datetime

from schematics.models import Model
from schematics.serialize import to_json, to_python
from schematics.types import DateTimeType, EmailType, IntType, LongType, SHA1Type, StringType
from schematics.types.compound import ModelType
from schematics.types.mongo import ObjectIdType

import tornado.gen


class message(object):
    def __init__(self, message_type):
        self.message_type = message_type

    def __call__(self, cls):
        setattr(cls, "_message_type", self.message_type)
        return cls


class collection_name(object):
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def __call__(self, cls):
        setattr(cls, "_collection_name", self.collection_name)
        return cls


class Document(Model):
    _id = ObjectIdType(minimized_field_name="_id")
    _dt = DateTimeType(minimized_field_name="_dt", required=True)

    def __init__(self, json_data=None, **kwargs):
        if json_data is not None:
            data = json.loads(json_data)
            super(Document, self).__init__(**data)
        else:
            super(Document, self).__init__(**kwargs)

        self.initialize()

    def initialize(self):
        # if hasattr(self, "_collection_name") is False:
        #     raise Exception("Document has no target collection. Use @collection_name decorator.")

        self._dt = datetime.datetime.utcnow()

        if self.timestamp is None:
            self.timestamp = int(time.time())

    def to_json(self, validate=False):
        if validate is True:
            self.validate()
        return to_json(self)

    def to_python(self, validate=False):
        if validate is True:
            self.validate()
        return to_python(self)

    @tornado.gen.coroutine
    def save(self, db_context, collection_name, validate=False):
        doc = self.to_python(validate)
        yield db_context.insert(collection_name=collection_name, doc=doc)
        raise tornado.gen.Return(doc)


class ClusterInfo(Model):
    name = StringType(minimized_field_name="name", required=True)
    db_name = StringType(minimized_field_name="db_name", required=True)


class ApplicationInfo(Document):
    name = StringType(minimized_field_name="name", max_length=100, required=True)
    cluster = ModelType(ClusterInfo, minimized_field_name="cluster", required=True)
    timestamp = IntType(minimized_field_name="ts")


class AccountInfo(Document):
    name = StringType(minimized_field_name="name", max_length=100, required=True)
    email = EmailType(minimized_field_name="email", max_length=100, required=True)
    password = SHA1Type(minimized_field_name="pwd", required=True)
    timestamp = IntType(minimized_field_name="ts")


class Message(Document):
    _mt = StringType(minimized_field_name="_mt", required=True)

    def initialize(self):
        super(Message, self).initialize()

        if self._mt is None:
            if hasattr(self, "_message_type") is True:
                self._mt = getattr(self, "_message_type")
            else:
                raise Exception("Message has no type information. Use @message decorator.")


# apa
@message("apa")
@collection_name("apa")
class ApplicationAdded(Message):
    """
    s: The UID of the user adding the application.
    u: A 16-digit unique hexadecimal string to track an invite, notification email, or stream post;
        generated if the user installed the application as a result of clicking on an invite,
        notification, email, or post. Valid characters are a-f, A-F, 0-9. This parameter must match
        the u parameter in the associated ins/inr, pst/psr, or nes/nei API calls that the install
        originated from.
    su: An 8-digit unique hexadecimal string. If a click is from an advertisement, link, or partner
        site, use this parameter instead of the u parameter. Valid characters are a-f, A-F, 0-9.
        This parameter must match the su parameter in the associated ucc API call.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The timestamp in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    user_uid = LongType(minimized_field_name="uuid", required=True)
    tracking_uid = StringType(minimized_field_name="tuid",
                              regex="[0-9A-Fa-f]+", min_length=8, max_length=16)
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# apr
@message("apr")
class ApplicationRemoved(Message):
    """
    s: The UID of the user removing the application.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The timestamp in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    user_uid = LongType(minimized_field_name="uuid", required=True)
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# cpu
@message("cpu")
class UserInformation(Message):
    """
    s: The UID of the user.
    b: The year of the user's birth, in YYYY/MM/DD format.
    g: The gender of the user. Accepted parameter values are: m (Male), f (Female),
        and u (Unknown, if no gender is specified).
    lc: The country code of the country in which the user is located. The country code must be in
        upper case format and conform to the ISO 3166-1 alpha-2 standard. If not sent, it will be
        based on the parameter included in the pgr message.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The timestamp in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    user_uid = LongType(minimized_field_name="uuid", required=True)
    birthday = StringType(minimized_field_name="b", min_length=10, max_length=10)
    gender = StringType(minimized_field_name="g", min_length=1, max_length=1)
    country = StringType(minimized_field_name="lc")
    friends_count = IntType(minimized_field_name="f")
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# evt
@message("evt")
class CustomEvent(Message):
    """
    s: The UID of the user.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The timestamp in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    user_uid = LongType(minimized_field_name="uuid", required=True)
    event_name = StringType(minimized_field_name="n", min_length=1, max_length=128, required=True)
    value = IntType(minimized_field_name="v", default=1)
    level = IntType(minimized_field_name="lv", default=1)
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# ins
@message("ins")
class InviteSent(Message):
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# inr
@message("inr")
class InviteReceived(Message):
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# gci
@message("gci")
class GoalCounts(Message):
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# mtu
@message("mtu")
class RevenueTracking(Message):
    """
    s: The UID of the user.
    u: The page address to be recorded can be set manually using this parameter. If this message is
        posted to the server directly from the end user's browser, it is not necessary to set this
        parameter, as the page address can be derived from the information in the HTTP header.
        The value of this parameter, if present, should be URL-encoded.
    ip: The IP address of the user requesting the page. If this message is sent to the Appspand API
        server directly from your server, you must set this parameter.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The timestamp in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    user_uid = LongType(minimized_field_name="uuid", required=True)
    event_name = StringType(minimized_field_name="n", min_length=1, max_length=128)
    value = IntType(minimized_field_name="v", required=True)
    level = IntType(minimized_field_name="lv", default=1)
    data = StringType()
    timestamp = IntType(minimized_field_name="ts")


# pgr
@message("pgr")
class PageRequest(Message):
    """
    s: The UID of the user.
    u: The page address to be recorded can be set manually using this parameter. If this message is
        posted to the server directly from the end user's browser, it is not necessary to set this
        parameter, as the page address can be derived from the information in the HTTP header.
        The value of this parameter, if present, should be URL-encoded.
    ip: The IP address of the user requesting the page. If this message is sent to the Appspand API
        server directly from your server, you must set this parameter.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The timestamp in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    user_uid = LongType(minimized_field_name="uuid", required=True)
    url = StringType(minimized_field_name="url", min_length=1, max_length=128)
    ip = StringType(min_length=1, max_length=32)
    data = StringType()
    timestamp = IntType(minimized_field_name="ts", required=True)


# pst
@message("pst")
class StreamPost(Message):
    pass


# psr
@message("psr")
class StreamResponse(Message):
    pass


# ucc
@message("ucc")
class ExternalLinkClick(Message):
    pass


# nes
@message("nes")
class NotificationEmailSent(Message):
    pass


# nei
@message("nei")
class NotificationEmailResponse(Message):
    pass
