import string
import random
import os
import json
import datetime

from flask_mail import Message
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.inspection import inspect
from flask import render_template


class AbstractAttribute(object):
    def __get__(self, obj, type):
        raise NotImplementedError(
            "Abstract attribute should be implemented in subclass")


def get_current_time():
    return datetime.datetime.utcnow()


def commit_or_rollback(session):
    try:
        session.commit()
    except (DBAPIError, IntegrityError):
        session.rollback()
        raise


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # return int(obj.strftime('%s'))
            return str(obj)
        elif isinstance(obj, datetime.date):
            # return int(obj.strftime('%s'))
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


def send_mail(mail, subject, user, phrases, product_insights):
    try:
        msg = Message(subject,
                      sender="pranto157@gmail.com",
                      recipients=[user.email])
        msg.html = render_template(
            'email.html', product_insights=product_insights, name=user.name, phrases=phrases)
        mail.send(msg)
    except Exception:
        raise
