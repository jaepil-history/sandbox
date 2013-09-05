import time
import datetime

import bson
from mongoengine import Document
from mongoengine import EmbeddedDocument
from mongoengine import DateTimeField
from mongoengine import EmbeddedDocumentField
from mongoengine import IntField
from mongoengine import LongField
from mongoengine import StringField
from mongoengine import EmailField
from password import PasswordField
from mongoengine import ValidationError

import tornado.gen


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
            except ValidationError:
                doc = ValidationError.to_dict()
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
    ul: The level of the user.
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


# cpu
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
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


# lgn
class Login(BaseDoc):
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

    _mt = StringField(default='lgn')
    user_uid = LongField(required=True, db_field='uuid')
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    timestamp = IntField(db_field='ts')
    # meta = {'collection': 'lgn'}


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


# mtu
class RevenueTracking(BaseDoc):
    """
    s: The UID of the user.
    data: Additional data, a JSON object string representing a dictionary or map of key-value pairs.
        It must be base64-encoded.
    ts: The ts in the Epoch time format.
        Include this parameter to prevent the user's browser from caching the REST API call if sent
        using JavaScript.
    """

    _mt = StringField(default='mtu')
    user_uid = LongField(required=True, db_field='uuid')
    event_name = StringField(min_length=1, max_length=128)
    value = IntField(required=True)
    level = IntField(required=True, default=1, db_field='lv')
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
    user_level = IntField(required=True, default=1, db_field='ul')
    friends_count = IntField(db_field='f')
    data = StringField()
    timestamp = IntField(db_field='ts')


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


# gci
class GoalCounts(BaseDoc):
    _mt = StringField(default='gci')
    data = StringField()
    timestamp = IntField(db_field='ts')

