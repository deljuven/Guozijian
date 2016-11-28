# -*- coding: utf-8 -*-
from guozijian import login_manager
from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators


def signin():
    pass


def signout():
    pass


def registration():
    pass


@login_manager.user_loader
def load_user(userid):
    # return User.get(userid)
    pass

class LoginForm(FlaskForm):
    username = StringField('User Name')
    passwd = PasswordField('Password')


class RegistrationForm(FlaskForm):
    username = StringField('User Name')
    email = StringField('email')
    passwd = PasswordField('New Password')
    confirm = PasswordField('Repeat Password')
