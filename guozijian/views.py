# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required
from flask_moment import Moment

from guozijian import app, login_manager
from login import signin, signout, signup
from models import User, LoginForm, RegistrationForm, CountInfo, ClassInfo, ClassForm
from service import test_db, snapshot, add_class, delete_class
from utils import PER_PAGE

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
    offset = request.args.get('offset', type=int)
    page = offset / PER_PAGE + 1
    data = CountInfo.query.paginate(page=page, per_page=PER_PAGE)
    return jsonify(total=data.total, data=[i.serialize for i in data.items])


@app.route('/class', methods=['GET', 'POST', 'PUT', 'DELETE'])
def class_():
    form = ClassForm()
    class_id = request.args.get('class', type=int)
    name = form.name
    begin = form.begin
    end = form.end
    days_of_week = form.days_of_week
    total = form.total
    app.logger.info(name.data)
    app.logger.info(begin.data)
    app.logger.info(end.data)
    app.logger.info(days_of_week.data)
    app.logger.info(total.data)
    if request.method == 'POST' and form.validate_on_submit():
        add_class(name=name.data, begin=begin.data, end=end.data, days_of_week=days_of_week.data, total=total.data)
        return redirect(url_for('class_list'))
    elif request.method == 'PUT' and form.validate_on_submit():
        # class_info = update_class(id=class_id, name=name.data, begin=begin.data, end=end.data,
        #                           days_of_week=days_of_week.data, total=total.data)
        # return render_template("class_modifier.html", form=form, class_info=class_info)
        app.logger.info(form.days_of_week.data)
    elif request.method == 'GET':
        if class_id is None:
            return redirect(url_for('class_list'))
        class_info = ClassInfo.query.get(class_id)
        return render_template("class_modifier.html", form=form, class_info=class_info)
    elif request.method == 'DELETE':
        if class_id is None:
            return redirect(url_for('class_list'))
        delete_class(class_id)
        return redirect(url_for('class_list'))


@app.route('/class_list')
def class_list():
    class_list = ClassInfo.query.all()
    return render_template("class_list.html", class_list=class_list)


@app.route('/classes')
def classes():
    class_list = ClassInfo.query.all()
    return jsonify(class_list)


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
    return test_db()


@app.route('/snapshot')
@login_required
def onSnapshot():
    snapshot()
    return jsonify(title="hello world")


@app.route('/latest')
@login_required
def latest():
    latest = CountInfo.query.order_by(CountInfo.taken_at.desc()).limit(100).all()
    return jsonify([i.serialize for i in latest])
