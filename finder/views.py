# -*- coding: utf-8 -*-
import base64
import os

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required
from flask_moment import Moment

from app import app, APP_IMG_SAV_PATH
from login import signin, signout, signup, login_manager
from models import LoginForm, RegistrationForm, User

moment = Moment(app)


def redirect_url(default='index'):
    return request.args.get('next') or request.referrer or url_for(default)


@app.route('/')
@login_required
def home():
    return redirect(url_for('index'))


@app.route('/index')
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.passwd.data
        if signin(name, password):
            return redirect(url_for('index'))
        return render_template("login.html", form=form)
    return render_template("login.html", form=form, users=User.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.username.data
        password = form.passwd.data
        email = form.email.data
        signup(name, password, email)
        return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/logout')
@login_required
def logout():
    signout()
    return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
@login_required
def search():
    return render_template('search.html')


@app.route('/upload', methods=['POST', 'OPTIONS'])
@login_required
def upload():
    if request.method == 'POST' and request.form.get("action") == "add":
        data = request.form.get("picStr")
        imgdata = base64.b64decode(data)
        imgfile = os.path.join(APP_IMG_SAV_PATH, 'pattern.png')
        file = open(imgfile, 'wb')
        file.write(imgdata)
        file.close()
        return jsonify({'status': 'ok'})


@app.route('/status', methods=['GET'])
@login_required
def status():
    # matcher = SurfMatcher()
    # flag, good = matcher.matches()
    # if flag:
    #     pass
    return render_template("status.html", index=2)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
