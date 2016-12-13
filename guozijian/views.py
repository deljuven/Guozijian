# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required
from flask_moment import Moment

from guozijian import app, login_manager
from login import signin, signout, signup
from models import User, LoginForm, RegistrationForm, CountInfo, ClassInfo, ClassForm
from service import snapshot, delete_class, add_class, update_class, query_counts
from utils import PER_PAGE, WEEKDAY_MAP

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


@app.route('/classes', methods=['GET', 'POST'])
def new_class():
    form = ClassForm()
    name = form.name
    begin = form.begin
    end = form.end
    days_of_week = form.days_of_week
    total = form.total
    if request.method == 'GET':
        return render_template("class_modifier.html", form=form)
    days_of_week.data = [int(t.encode("ascii")) for t in days_of_week.data]
    tmp = {t: WEEKDAY_MAP[t] for t in days_of_week.data}
    if request.method == 'POST' and form.validate_on_submit():
        add_class(name=name.data, begin=begin.data, end=end.data, days_of_week=days_of_week.data, total=total.data)
        return redirect(url_for('class_list'))
    return render_template("class_modifier.html", form=form)


@app.route('/classes/<class_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def change_class(class_id):
    form = ClassForm()
    name = form.name
    begin = form.begin
    end = form.end
    days_of_week = form.days_of_week
    total = form.total
    class_info = ClassInfo.query.get(class_id)
    if request.method == 'DELETE':
        if class_id is None:
            return "failed"
        delete_class(class_id)
        return "success"
    elif request.method == "GET":
        return render_template("class_modifier.html", form=form, class_info=class_info, class_id=class_id)
    days_of_week.data = [int(t.encode("ascii")) for t in days_of_week.data]
    tmp = {t: WEEKDAY_MAP[t] for t in days_of_week.data}
    if request.method == 'POST' and request.form['_method'] == 'PUT' and form.validate_on_submit():
        class_info = update_class(class_id=class_id, name=name.data, begin=begin.data, end=end.data,
                                  days_of_week=days_of_week.data, total=total.data)
        return render_template("class_modifier.html", form=form, class_info=class_info, class_id=class_id)
    elif request.method == 'PUT':
        # class_info = update_class(id=class_id, name=name.data, begin=begin.data, end=end.data,
        #                           days_of_week=days_of_week.data, total=total.data)
        # return render_template("class_modifier.html", form=form, class_info=class_info)
        # class_info = ClassInfo.query.get(class_id)
        if form.validate_on_submit():
            class_info = update_class(class_id=class_id, name=name.data, begin=begin.data, end=end.data,
                                      days_of_week=days_of_week.data, total=total.data)
            return jsonify(class_info.serialize)
        return jsonify(form.errors)
    return render_template("class_modifier.html", form=form, class_info=class_info, class_id=class_id)


@app.route('/classes/')
@app.route('/classes/list')
def class_page():
    offset = request.args.get('offset', type=int, default=0)
    per_page = request.args.get('limit', type=int, default=PER_PAGE)
    search = request.args.get('search')
    page = offset / per_page + 1
    query = ClassInfo.query
    if search:
        query = query.filter(ClassInfo.name.like("%%%s%%" % search))
    data = query.paginate(page=page, per_page=per_page)
    return jsonify(total=data.total, data=[i.serialize for i in data.items])


@app.route('/class_list')
def class_list():
    return render_template("class_list.html")


@app.route('/statistic')
@login_required
def statistic():
    class_id = request.args.get('class', type=int)
    if class_id is None:
        return redirect(url_for('class_list'))
    count = CountInfo.query.filter_by(class_id=class_id).first()
    return render_template("statistic.html", count=count, class_id=class_id)


@app.route('/counts')
@login_required
def counts():
    class_id = request.args.get('class', type=int)
    offset = request.args.get('offset', type=int, default=0)
    per_page = request.args.get('limit', type=int, default=PER_PAGE)
    name = request.args.get('name')
    begin = request.args.get('begin', type=float)
    end = request.args.get('end', type=float)
    page = offset / per_page + 1
    data = query_counts(begin=begin, end=end, class_id=class_id, name=name, page=page, per_page=per_page)
    return jsonify(total=data.total, data=[i.serialize for i in data.items])


@app.route('/snapshot')
@login_required
def on_snapshot():
    class_id = request.args.get('class', type=int)
    snapshot(class_id)
    return jsonify(title="hello world")


@app.route('/latest')
@login_required
def latest():
    latest = CountInfo.query.order_by(CountInfo.taken_at.desc()).limit(100).all()
    return jsonify([i.serialize for i in latest])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
