# -*- coding: utf-8 -*-
from flask import flash, session
from flask_login import login_user, logout_user

from guozijian import login_manager, db
from models import User


def signin(username, passwd, form):
    user = User.query.filter_by(name=username, password=passwd).first()
    if user is None:
        session.pop('_flashes', None)
        flash("Incorrect username or password")
        return False
    login_user(user)
    return True


def signout():
    logout_user()


def signup(username, passwd, email):
    user = User(username, passwd, email)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    login_user(user)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
