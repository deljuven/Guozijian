# -*- coding: utf-8 -*-
from flask import render_template, flash
from flask_login import login_user

from guozijian import login_manager, db, app
from models import User


def signin(username, passwd, form):
    user = User.query.filter_by(name=username, password=passwd).first()
    if user is None:
        return render_template("login.html", form=form, message="Incorrect username or password")
    login_user(user)
    flash('Logged in successfully.')


def signout():
    pass


def registration(username, passwd, email):
    user = User(username, passwd, email)
    db.session.add(user)
    db.session.commit()
    flash('Thanks for registering')


@login_manager.user_loader
def load_user(userid):
    # return User.get(userid)
    pass
