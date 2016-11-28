# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from flask_moment import Moment

from guozijian import app, db
from login import signin, signout, registration
from models import User, LoginForm, RegistrationForm

moment = Moment(app)


@app.route('/')
def home():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.passwd.data
        signin(name, password, form)
        next = request.args.get('next')
        return redirect(next or url_for('index'))
    return render_template("login.html", form=form, users=User.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    message = None
    if form.validate_on_submit():
        name = form.username.data
        password = form.passwd.data
        email = form.email.data
        registration(name, password, email)
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


@app.route('/auth/logout')
def logout():
    signout()
    return redirect(url_for('login'))


@app.route('/flot')
def flot():
    return render_template("flot.html")


@app.route('/morris')
def morris():
    return render_template("morris.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/test')
def test():
    return render_template("blank.html")


@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'
