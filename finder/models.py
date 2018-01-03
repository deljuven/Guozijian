# -*- coding: utf-8 -*-

from flask_user import UserMixin
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, validators, BooleanField, FileField, SubmitField

from database import db


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
