# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required
from flask_moment import Moment

from guozijian import app, db, login_manager
from login import signin, signout, signup
from models import User, LoginForm, RegistrationForm, CountInfo
from utils import PER_PAGE

moment = Moment(app)


@app.route('/')
@login_required
def home():
    return redirect(url_for('index'))


@app.route('/index')
@login_required
def index():
    counts = CountInfo.query.all()
    return render_template("index.html", counts=counts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        password = form.passwd.data
        if signin(name, password, form):
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


@app.route('/counts')
@login_required
def counts():
    page = request.args.get('page')
    app.logger.info(page)
    data = CountInfo.query.paginate(page=page, per_page=PER_PAGE)
    # cur_page = json.dumps([obj.__dict__ for obj in data.items])
    app.logger.info(data.items)
    return jsonify(total=data.total, data=[i.serialize for i in data.items])
    # return render_template("teacherSelector.html", pagination=data)


@app.route('/flot')
def flot():
    return render_template("flot.html")


@app.route('/morris')
def morris():
    return render_template("morris.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/testdb')
def testdb():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


@app.route('/snapshot')
@login_required
def snapshot():
    # liran use for test here
    return jsonify(title="hello world")
