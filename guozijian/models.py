# -*- coding: utf-8 -*-
from flask_user import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField

from guozijian import db


class LoginForm(FlaskForm):
    username = StringField('User Name', [validators.DataRequired()])
    passwd = PasswordField('Password', [validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('User Name', [validators.DataRequired()])
    email = StringField('email', [validators.DataRequired()])
    passwd = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the ToS', [validators.DataRequired()])


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(100), unique=True, nullable=False)
    password = db.Column("passwd", db.String(100), nullable=False)
    email = db.Column("email", db.String(100), unique=True, nullable=False)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % {'name': self.name.encode(), 'email': self.email.encode()}

    def is_authenticated(self):
        return True

    def is_actice(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return "1"

    def get(user_id):
        pass


class CountInfo(db.Model):
    __tablename__ = 'count_info'
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column("name", db.String(100), unique=True, nullable=False)
    uri = db.Column("uri", db.String(200), unique=True, nullable=False)
    taken_at = db.Column("taken_at", db.DateTime, nullable=False)
    count = db.Column("count", db.Integer)

    def __init__(self, name, uri, taken_at, count=None):
        self.name = name
        self.uri = uri
        self.taken_at = taken_at
        self.count = count

    def __repr__(self):
        return '<User %r>' % {'name': self.name.encode(), 'uri': self.uri.encode()}

