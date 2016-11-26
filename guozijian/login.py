# -*- coding: utf-8 -*-
from guozijian import login_manager
from models import User
from flask_wtf import Form
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

class LoginForm(Form):
    username = StringField('name', [validators.Length(min=4, max=25)])
    confirm = PasswordField('password', validators.DataRequired())
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class RegistrationForm(Form):
    username = StringField('name', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
