# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from flask_moment import Moment
from flask_socketio import emit, join_room, leave_room

from app import app, APP_IMG_SAV_PATH, APP_PATH, socketio
from login import signin, signout, signup, login_manager
from models import User, LoginForm, RegistrationForm, CountInfo, ClassInfo, ClassForm
from service import delete_class, add_class, update_class, query_counts, query_class, read_msgs, snapshot
from utils import PER_PAGE, DEFAULT_NOTIFICATION, REFRESH_NOTIFICATION

# import eventlet
# eventlet.monkey_patch()

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
    return render_template("index.html", user=current_user.user_id)


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


@app.route('/classes', methods=['GET', 'POST'])
@login_required
def new_class():
    form = ClassForm()
    name = form.name
    begin = form.begin
    end = form.end
    days_of_week = form.days_of_week
    total = form.total
    interval = form.interval
    if request.method == 'GET':
        return render_template("class_modifier.html", form=form)
    days_of_week.data = [int(t.encode("ascii")) for t in days_of_week.data]
    if request.method == 'POST' and form.validate_on_submit():
        add_class(name=name.data, begin=begin.data, end=end.data, days_of_week=days_of_week.data, total=total.data,
                  img_path=APP_IMG_SAV_PATH, app_path=APP_PATH, creator=current_user.user_id, interval=interval.data)
        return redirect(url_for('class_list'))
    return render_template("class_modifier.html", form=form)


@app.route('/classes/<class_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def change_class(class_id):
    form = ClassForm()
    name = form.name
    begin = form.begin
    end = form.end
    days_of_week = form.days_of_week
    total = form.total
    interval = form.interval
    class_info = ClassInfo.query.get(class_id)
    if request.method == 'DELETE':
        if class_id is None:
            return "failed"
        delete_class(class_id)
        return "success"
    elif request.method == "GET":
        return render_template("class_modifier.html", form=form, class_info=class_info, class_id=class_id)
    days_of_week.data = [int(t.encode("ascii")) for t in days_of_week.data]
    if request.method == 'POST' and request.form['_method'] == 'PUT' and form.validate_on_submit():
        class_info = update_class(class_id=class_id, name=name.data, begin=begin.data, end=end.data,
                                  days_of_week=days_of_week.data, total=total.data, img_path=APP_IMG_SAV_PATH,
                                  app_path=APP_PATH, interval=interval.data)
        return render_template("class_modifier.html", form=form, class_info=class_info, class_id=class_id)
    elif request.method == 'PUT':
        if form.validate_on_submit():
            class_info = update_class(class_id=class_id, name=name.data, begin=begin.data, end=end.data,
                                      days_of_week=days_of_week.data, total=total.data, img_path=APP_IMG_SAV_PATH,
                                      app_path=APP_PATH, interval=interval.data)
            return redirect(url_for('class_list'))
        return jsonify(form.errors)
    return render_template("class_modifier.html", form=form, class_info=class_info, class_id=class_id)


@app.route('/classes/')
@app.route('/classes/list')
@login_required
def class_page():
    offset = request.args.get('offset', type=int, default=0)
    per_page = request.args.get('limit', type=int, default=PER_PAGE)
    search = request.args.get('search')
    class_id = request.args.get('class')
    page = offset / per_page + 1
    query = ClassInfo.query
    if class_id:
        return jsonify(query.get(class_id).serialize)
    data = query_class(name=search, creator=current_user.user_id, page=page, per_page=per_page)
    return jsonify(total=data.total, data=[i.serialize for i in data.items])


@app.route('/class_list')
@login_required
def class_list():
    return render_template("class_list.html")


@app.route('/statistic')
@login_required
def statistic():
    class_id = request.args.get('class', type=int)
    if class_id is None:
        return redirect(url_for('class_list'))
    count = CountInfo.query.filter_by(class_id=class_id).order_by(CountInfo.count_id.desc()).first()
    class__ = ClassInfo.query.get(class_id)
    if class__:
        total = class__.total
        return render_template("statistic.html", count=count, class_id=class_id, total=total)
    return redirect(url_for('class_list'))


@app.route('/counts')
@login_required
def counts():
    class_id = request.args.get('class', type=int)
    offset = request.args.get('offset', type=int, default=0)
    per_page = request.args.get('limit', type=int, default=-1)
    name = request.args.get('name')
    begin = request.args.get('begin', type=float)
    end = request.args.get('end', type=float)
    last = request.args.get('last', type=int)
    page = offset / per_page + 1
    data = query_counts(begin=begin, end=end, class_id=class_id, name=name, last=last, page=page, per_page=per_page)
    items = data['data']
    return jsonify(total=data['total'], data=[i.serialize for i in items])


@app.route('/snapshot')
@login_required
def on_snapshot():
    class_id = request.args.get('class', type=int)
    faces = snapshot(class_id, APP_IMG_SAV_PATH, APP_PATH)
    # faces = 1
    total = ClassInfo.query.get(class_id).total
    if faces < total - 1:
        app.logger.info('snap test')
    return jsonify(faces)


@app.route('/latest')
@login_required
def latest():
    latest_ = CountInfo.query.order_by(CountInfo.taken_at.desc()).limit(100).all()
    return jsonify([i.serialize for i in latest_])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route("/msg")
def messages():
    return jsonify({'msgs': read_msgs(current_user.user_id)})


@socketio.on('connect', namespace=DEFAULT_NOTIFICATION)
def notification_connect():
    return True
    # emit('connect', {'data': 'Connected'}, namespace=DEFAULT_NOTIFICATION)
    # if current_user.is_authenticated:
    # emit('connect', {'data': 'Connected'}, namespace=DEFAULT_NOTIFICATION)
    # room = json['user']
    # join_room(room)
    # emit('connect', {'data': 'Connected %d' % room}, namespace=DEFAULT_NOTIFICATION)
    # else:
    #     return False


@socketio.on('disconnect', namespace=DEFAULT_NOTIFICATION)
def notification_disconnect():
    # room = json['user']
    # leave_room(room)
    print 'Disconnected %d' % 123
    # emit('disconnect', {'data': 'Disconnected %d' % room}, namespace=DEFAULT_NOTIFICATION)


@socketio.on('connect', namespace=REFRESH_NOTIFICATION)
def snapshot_connect():
    if current_user.is_authenticated:
        emit('connect', {'data': 'Connected'}, namespace=REFRESH_NOTIFICATION)
    else:
        return False


@socketio.on('join', namespace=REFRESH_NOTIFICATION)
def snapshot_join(room):
    join_room(room)
    emit('join', {'data': 'Join room %d' % room}, namespace=REFRESH_NOTIFICATION)


@socketio.on('leave', namespace=REFRESH_NOTIFICATION)
def snapshot_leave(room):
    leave_room(room)
    emit('leave', {'data': 'Leave room %d' % room}, namespace=REFRESH_NOTIFICATION)


@socketio.on('disconnect', namespace=REFRESH_NOTIFICATION)
def snapshot_disconnect():
    print 'Disconnected %d' % 123


@socketio.on('warning', namespace=DEFAULT_NOTIFICATION)
def warning(json):
    msgs = read_msgs(json.user_id)
    emit('warning', {'data': [msg.serialize for msg in msgs]}, namespace=DEFAULT_NOTIFICATION)
