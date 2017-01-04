# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime

from flask_user import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField, IntegerField, SelectMultipleField, \
    ValidationError

from database import db
from utils import WEEKDAYS, WEEKDAY_MAP


class LoginForm(FlaskForm):
    username = StringField(u'用户名', [validators.DataRequired()])
    passwd = PasswordField(u'密码', [validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField(u'用户名', [validators.DataRequired()])
    email = StringField(u'电子邮箱', [validators.DataRequired()])
    passwd = PasswordField(u'密码', [
        validators.DataRequired(),
        validators.EqualTo(u'确认密码', message=u'密码必须匹配')
    ])
    confirm = PasswordField(u'确认密码')
    accept_tos = BooleanField(u'我已经阅读服务条款并接受', [validators.DataRequired()])


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(100), unique=True, nullable=False)
    password = db.Column("passwd", db.String(100), nullable=False)
    email = db.Column("email", db.String(100), unique=True, nullable=False)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % {'name': self.name.encode(), 'email': self.email.encode()}

    @property
    def serialize(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email
        }

    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def get(user_id):
        User.query.get(user_id)


class CountInfo(db.Model):
    __tablename__ = 'count_info'
    count_id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(100), unique=True, nullable=False)
    uri = db.Column("uri", db.String(200), unique=True, nullable=False)
    taken_at = db.Column("taken_at", db.DateTime, nullable=False)
    count = db.Column("count", db.Integer)
    class_id = db.Column("class_id", db.Integer)

    def __init__(self, name, uri, taken_at, count=None, class_id=None):
        self.name = name
        self.uri = uri
        self.taken_at = taken_at
        self.count = count
        self.class_id = class_id

    def __repr__(self):
        return '<Count %r>' % {'id': self.count_id, 'name': self.name.encode(), 'uri': self.uri.encode(),
                               'taken_at': self.taken_at, 'count': self.count, 'class_id': self.class_id}
        # return json.dumps(self.__dict__)

    @property
    def serialize(self):
        return {
            "id": self.count_id,
            "name": self.name,
            "uri": self.uri,
            "taken_at": self.taken_at,
            "count": self.count,
            "class_id": self.class_id
        }


class ClassInfo(db.Model):
    __tablename__ = 'class'
    class_id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(100), unique=True, nullable=False)
    begin = db.Column("begin_time", db.String(20), nullable=False)
    end = db.Column("end_time", db.String(20), nullable=False)
    days_of_week = db.Column("days_of_week", db.String(30), nullable=False)
    total = db.Column("total", db.Integer, nullable=False)
    interval = db.Column("interval", db.Integer, nullable=False, default=5)
    creator = db.Column("creator", db.Integer, nullable=False)

    def __init__(self, name, begin, end, days_of_week, total, creator, interval=5):
        self.name = name
        self.begin = begin
        self.end = end
        self.days_of_week = json.dumps(days_of_week)
        self.total = total
        self.interval = interval
        self.creator = creator

    def __repr__(self):
        return '<Class %r>' % {'name': self.name.encode(), 'begin': self.begin.encode(), 'end': self.end.encode(),
                               'days_of_week': json.loads(self.days_of_week), 'total': self.total,
                               'interval': self.interval}

    @property
    def serialize(self):
        days = map(lambda x: WEEKDAY_MAP[x], json.loads(self.days_of_week))
        return {
            "id": self.class_id,
            "name": self.name,
            "begin": self.begin,
            "end": self.end,
            "days_of_week": days,
            "days": self.days_of_week,
            "total": self.total,
            "interval": self.interval
        }


TIME_FORMAT = "%H:%M"


def begin_end_validate(field_name=None, message=None):
    msg = "Begin should be before end" if message is None else message

    def _begin_end_validate(form, field):
        try:
            begin_field = form[field_name]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % field_name)
            # begin = begin_field.data.split(":")
            # end = field.data.split(":")
            # if not (int(begin[0]) < int(end[0]) and int(begin[1]) < int(end[1])):
        begin = time.strptime(begin_field.data, TIME_FORMAT)
        end = time.strptime(field.data, TIME_FORMAT)
        if not begin < end:
            raise ValidationError(msg)

    return _begin_end_validate


class ClassForm(FlaskForm):
    name = StringField(label=u'课程名称', validators=[validators.DataRequired()])
    begin = StringField(label=u'开始时间', validators=[validators.DataRequired(), validators.Regexp("\d{1,2}:\d{2}")])
    end = StringField(
        label=u'结束时间',
        validators=[validators.DataRequired(), validators.Regexp("\d{1,2}:\d{2}"), begin_end_validate('begin', "test")])
    days_of_week = SelectMultipleField(label=u'每周上课时间', choices=WEEKDAYS,
                                       validators=[validators.DataRequired()])
    total = IntegerField(label=u'班级人数', validators=[validators.DataRequired()])
    interval = IntegerField(label=u'拍照频率(分钟)', validators=[validators.DataRequired()])
