import time
import datetime

import bson
from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import DateTimeField
from mongoengine import EmbeddedDocumentField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import FloatField
from mongoengine import StringField
from mongoengine import ListField
from mongoengine import BooleanField
from mongoengine import EmailField
from password import PasswordField
from mongoengine import ValidationError

import tornado.gen

MAX_RETENTION_DAYS = 28

class BaseDoc(Document):
    _dt = DateTimeField(required=True)

    def __init__(self, *args, **values):
        super(Document, self).__init__(*args, **values)
        self.initialize()

    def initialize(self):
        self._dt = datetime.datetime.utcnow()
        # ts : timestamp
        if self.timestamp is None:
            self.timestamp = int(time.time())

    def to_python(self):
        data = self.to_mongo()
        data = bson.son.SON(data).to_dict()
        del(data['_cls'])
        return data

    @tornado.gen.coroutine
    def save(self, db_context, collection_name, validate=False):
        if validate:
            try:
                self.validate()
            except ValidationError as e:
                doc = e.to_dict()
                raise tornado.gen.Return(doc)

        doc = self.to_python()
        yield db_context.insert(collection_name=collection_name, doc=doc)
        raise tornado.gen.Return(doc)

    meta = {'allow_inheritance': True}


class ClusterInfo(EmbeddedDocument):
    name = StringField(required=True, max_length=100)
    db_name = StringField(required=True, max_length=100)


class ApplicationInfo(BaseDoc):
    name = StringField(max_length=100, required=True)
    cluster = EmbeddedDocumentField(ClusterInfo)
    timestamp = IntField(db_field='ts')
    # meta = {'collection': 'application'}


class AccountInfo(BaseDoc):
    name = StringField(max_length=100, required=True)
    email = EmailField(max_length=100, required=True)
    password = PasswordField(algorithm="sha1")
    timestamp = IntField(db_field='ts')
    # meta = {'collection': 'account'}


# apa
class ApplicationAdded(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user. Installation or reinstallation
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='apa')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    created_at = DateTimeField(required=True, db_field='c')
    data = StringField()
    timestamp = IntField(db_field='ts')
    # meta = {'collection': 'apa'}


# apr
class ApplicationRemoved(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='apr')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


# usr
class User(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user. Installation or reinstallation
    f: The number of friends a user has.
    c: created datetime
    l_in: last login datetime
    ln: login count a day
    w: withdrawal
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    created_at = DateTimeField(required=True, db_field='c')
    last_login_at = DateTimeField(required=True, db_field='l_in')
    logins_a_day = ListField(IntField(), default=lambda: [0 for x in range(MAX_RETENTION_DAYS)], db_field='ln')
    withdrawal = BooleanField(default=False, db_field='w')
    last_purchase_at = DateTimeField(db_field='p')
    timestamp = IntField(db_field='ts')
    # meta = {'collection': 'usr'}


# cpu : sends user information in a common place in your application, such as a landing page or post-login page,
# and include the call to send this cpu message on these pages. Additionally, we recommend a cookie is also set to check
# if the user data was retrieved and sent for that day.
class UserInformation(BaseDoc):
    """
    s: The UID of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='cpu')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


# lgt
class Logout(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='lgt')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    timestamp = IntField(db_field='ts')
    # meta = {'collection': 'lgt'}


# wid
class Withdrawal(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='wid')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    timestamp = IntField(db_field='ts')
    # meta = {'collection': 'wid'}


# icu :  to track the consumption of items by users.
class ItemConsumption(BaseDoc):
    """
    s: The UID of the user.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='icu')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    item_id = IntField(required=True, db_field='iid')
    data = StringField()
    timestamp = IntField(db_field='ts')


# mtu :  to track revenue and monetization transactions by users.
class RevenueTracking(BaseDoc):
    """
    s: The UID of the user.
    cu : currency. USD:0, KWN:1, YEN:2, ...etc
    v: The revenue value which must be passed in cents.
        Example: $1.25 should be passed as 125. Can be either a positive or negative integer.
        The maximum value that can be passed is 1000000 ($10,000).
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='mtu')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    item_id = IntField(required=True, db_field='iid')
    currency = IntField(required=True, db_field='cu') # USD:0, KWN:1, YEN:2, ...
    value = IntField(required=True, db_field='v')
    data = StringField()
    timestamp = IntField(db_field='ts')


# ins
class InviteSent(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='ins')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


# rcv
class MessageReceived(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='msr')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


# its
class ItemSent(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='its')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    item_id = IntField(required=True, db_field='iid')
    data = StringField()
    timestamp = IntField(db_field='ts')


# itr
class ItemReceived(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='itr')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    item_id = IntField(required=True, db_field='iid')
    data = StringField()
    timestamp = IntField(db_field='ts')


# igr
class InGameResult(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='itr')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


# pgr
class PageRequest(BaseDoc):
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
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='pgr')
    user_uid = LongField(required=True, db_field='uuid')
    url = StringField(min_length=1, max_length=128)
    ip = StringField(min_length=1, max_length=32)
    data = StringField()
    timestamp = IntField(db_field='ts',required=True)

# inr
class InviteReceived(BaseDoc):
    """
    s: The UID of the user adding the application.
    ul: The level of the user.
    f: The number of friends a user has.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='inr')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


# evt
class CustomEvent(BaseDoc):
    """
    s: The UID of the user.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='evt')
    user_uid = LongField(required=True, db_field='uuid')
    event_name = StringField(min_length=1, max_length=128, required=True)
    value = IntField(default=1)
    level = IntField(default=1, db_field='lv')
    data = StringField()
    timestamp = IntField(db_field='ts')


# gci
class GoalCounts(BaseDoc):
    _mt = StringField(default='gci')
    user_uid = LongField(required=True, db_field='uuid')
    data = StringField()
    timestamp = IntField(db_field='ts')

