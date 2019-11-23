# coding: utf-8
"""Generated sqlacodegen postgresql://username:password@hostname/database"""

import datetime

from api.version1_0.authentication.security import common
from conf import settings

from collections import OrderedDict
from itsdangerous import (TimedJSONWebSignatureSerializer as SecSerializer,
                          BadSignature, SignatureExpired)

from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Float, \
    Integer, String, Table, Time, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Serializer(object):
    """Serialize information from database to a JSON Dictionary."""

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class AutoSerialize(object):
    """
        Mixin for retrieving public fields of model in json-compatible format'
    """
    __public__ = None

    def get_public(self, exclude=(), extra=()):
        """

        :param exclude:
        :param extra:
        :return:
        """
        data = {}
        keys = self._sa_instance_state.attrs.items()
        public = self.__public__ + extra if self.__public__ else extra
        for k, field in keys:
            if public and k not in public: continue
            if k in exclude: continue
            value = self._serialize(field.value)
            if value:
                data[k] = value
        return data

    @classmethod
    def _serialize(cls, value, follow_fk=False):
        if type(value) in (datetime,):
            ret = value.isoformat()
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                ret.append(cls._serialize(v))
        elif AutoSerialize in value.__class__.__bases__:
            ret = value.get_public()
        else:
            ret = value

        return ret


class DictSerializable(object):
    """

    """

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


class ApiUsers(db.Model, AutoSerialize, Serializer):
    __tablename__ = 'api_users'

    id = Column(Integer, primary_key=True, unique=True,
                server_default=text("nextval('api_users_id_seq'::regclass)"))
    username = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    created = Column(TIMESTAMP(True, 6))

    def __init__(self, username, password, created):
        """

        :param username:
        :param password:
        :param created:
        :return:
        """
        self.username = username
        self.password_hash = self.hash_password(password)
        self.created = created

    def hash_password(self, password):
        """Converts password (clear text) information into a hash password.

        :param password:
        :return:
        """
        return common.encrypt(password)

    def verify_password(self, password):
        """Verifies password (clear text) is the same as the one stored in
        hashed format.

        :param password:
        :return:
        """
        if password:
            if common.decrypt(self.password_hash) == password:
                return True
            else:
                return False

        return False

    def generate_auth_token(self, expiration=settings.TOKEN_EXPIRATION_SECS):
        """Generates a token.

        :param expiration: (int) Expiration time in seconds.
        :return: A token from (TimedJSONWebSignatureSerializer)
        """

        s = SecSerializer(
            settings.API_KEY,
            expires_in=expiration
        )
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """Check if there is a user with in database with obtained id.

            If True then access is granted,
            else user cannot access data.

        :param token: (str) Token information for user
        """

        s = SecSerializer(settings.API_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # Valid token, but expired. # TODO(gogasca) Add
            # logging.warning
        except BadSignature:
            return None  # Invalid token. # TODO(gogasca) Add logging.error
        user = ApiUsers.query.get(data['id'])
        return user

    def serialize(self):
        """Return user information from database."""

        d = Serializer.serialize(self)
        del d['password_hash']
        return d


class Campaign(db.Model, AutoSerialize, Serializer):
    __tablename__ = 'campaign'

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('campaign_id_seq'::regclass)"))
    description = Column(String(256))
    reference = Column(String(32), nullable=False)
    campaign_start = Column(TIMESTAMP(precision=6))
    campaign_end = Column(TIMESTAMP(precision=6))
    is_cancelled = Column(Boolean, server_default=text("false"))
    status = Column(Integer, server_default=text("0"))
    request_data = Column(String(4096))
    provider = Column(String(256))
    report = Column(Boolean, server_default=text("false"))
    is_test = Column(Boolean, server_default=text("false"))
    articles = Column(Integer)

    def serialize(self):
        """

        :return:
        """
        d = Serializer.serialize(self)
        del d['id']
        del d['description']
        del d['is_cancelled']
        del d['request_data']
        del d['status']
        return d

    def __init__(self, status, description, reference, start, request_data,
                 provider, report, articles, test):
        """

        :param status:
        :param description:
        :param reference:
        :param start:
        :param request_data:
        :param provider:
        :param report:
        :param test:
        :return:
        """
        self.status = status
        self.description = description
        self.reference = reference
        self.campaign_start = start
        self.request_data = request_data
        self.provider = provider
        self.report = report
        self.articles = articles
        self.is_test = test


class Company(db.Model, AutoSerialize, Serializer):
    __tablename__ = 'companies'

    company_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('company_company_id_seq'::regclass)"))
    name = Column(String(1024), nullable=False)
    Column('mention_date', Time)

    def serialize(self):
        """

        :return:
        """
        d = Serializer.serialize(self)
        return d

    def __init__(self, name):
        self.company_name = name


class News(db.Model, AutoSerialize, Serializer):
    __tablename__ = 'news'

    news_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('news_news_id_seq'::regclass)"))
    source = Column(String(64))
    source_id = Column(String(64))
    author = Column(String(128))
    title = Column(String(256), nullable=False)
    description = Column(String(65536))
    url = Column(String(512))
    url_to_image = Column(String(512))
    published_at = Column(Date())
    content = Column(String(65536))
    campaign = Column(String(16))
    score = Column(Float(53))
    magnitude = Column(Float(53))
    sentiment = Column(String(16))
    rank_score = Column(Float(53))
    rank_order = Column(Integer)
    translated_content = Column(String(65536))
    detected_language = Column(String(128))
    inserted_at = Column(DateTime(True))

    def serialize(self):
        """

        :return:
        """
        d = Serializer.serialize(self)
        del d['news_id']
        return d

    def __init__(self, title, content, url, source):
        """

        :param title:
        :param content:
        :param url:
        :param source:
        :return:
        """
        self.published_at = 'now()'
        self.title = title
        self.content = content
        self.url = url
        self.source = source


class Person(db.Model, AutoSerialize, Serializer):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('persons_id_seq'::regclass)"))
    name = Column(String(64), nullable=False)
    mention_date = Column(TIMESTAMP(True, 6))
    valid = Column(Boolean, server_default=text("true"))

    def serialize(self):
        """

        :return:
        """
        d = Serializer.serialize(self)
        del d['id']
        del d['mention_date']
        del d['valid']
        return d

    def __init__(self, name, mention_date):
        self.name = name
        self.mention_date = mention_date


t_tags = Table(
    'tags', metadata,
    Column('tag_id', Integer, nullable=False,
           server_default=text("nextval('tags_tag_id_seq'::regclass)")),
    Column('tag_name', String(128), nullable=False)
)

t_tags_news = Table(
    'tags_news', metadata,
    Column('tag_id', BigInteger),
    Column('news_id', BigInteger)
)
