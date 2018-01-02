# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request
from flask_login import login_required
from flask_moment import Moment
from flask_uploads import UploadSet, configure_uploads, IMAGES, \
    patch_request_class

from app import app
from login import signin, signout, signup, login_manager
from models import LoginForm, RegistrationForm, User

moment = Moment(app)
photos = UploadSet('photos', IMAGES + tuple("mp4"))
configure_uploads(app, photos)
patch_request_class(app)


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


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'], name="match.jpg")
        file_url = photos.url(filename)
        return redirect(url_for('search'))
    return render_template("search.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
