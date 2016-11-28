# -*- coding: utf-8 -*-
from flask_user import UserMixin

from guozijian import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), unique=True)
    password = db.Column("passwd", db.String(100))
    email = db.Column("email", db.String(100), unique=True)

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
