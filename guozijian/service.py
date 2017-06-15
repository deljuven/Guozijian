# -*- coding: utf-8 -*-
import json
import os
import time
from datetime import datetime, date

import eventlet
from flask_socketio import emit

from app import app
from database import db
from face.ImageDetector import ImageDetector
from models import CountInfo, ClassInfo, Message
from scheduler import scheduler
from utils import PER_PAGE, RETRY, WARN_LEVEL, WARN_EVENT, DEFAULT_NOTIFICATION, SNAPSHOT, SNAPSHOT_NEW, \
    REFRESH_NOTIFICATION, INTERVAL
from video.VideoService import VideoService, VideoException


def snapshot(class_id, img_path, app_path):
    vs = VideoService()
    try:
        url = vs.take_picture(RETRY)
    except VideoException as e:
        return {'success': False, 'err': e.message}
    detector = ImageDetector(url, img_path)
    faces = detector.detect(4)
    count = save_to_db(detector, faces, class_id, app_path)
    class_info = ClassInfo.query.get(class_id)
    broadcast(class_info, count)


def save_to_db(detector, face_count, class_id, app_path):
    name = os.path.basename(detector.file_path)
    path = os.path.relpath(detector.file_path, app_path)
    count = CountInfo(name, path, datetime.now(), face_count, class_id)
    db.session.add(count)
    db.session.flush()
    db.session.commit()
    return count


def add_class(name, begin, end, days_of_week, total, img_path, app_path, creator, interval=5):
    class_info = ClassInfo(name, begin, end, days_of_week, total, creator, interval=interval)
    db.session.add(class_info)
    db.session.flush()
    db.session.commit()
    today = datetime.today()
    if today.weekday() in json.loads(class_info.days_of_week):
        args = [img_path, app_path]
        begin = map(int, begin.split(":"))
        end = map(int, end.split(":"))
        start = today.replace(hour=begin[0], minute=begin[1] % 60)
        fin = today.replace(hour=end[0], minute=end[1] % 60)
        args = [class_info.class_id] + args
        job_id = '%d-%d' % (class_info.class_id, int(time.mktime(date(today.year, today.month, today.day).timetuple())))
        add_job(snapshot_job, args, job_id, start, fin, interval)
    return class_info


def update_class(class_id, name, begin, end, days_of_week, total, img_path, app_path, interval):
    class_info = ClassInfo.query.get(class_id)
    class_info.name = name
    class_info.begin = begin
    class_info.end = end
    class_info.days_of_week = json.dumps(days_of_week)
    class_info.total = total
    class_info.interval = interval
    db.session.commit()
    today = datetime.today()
    if today.weekday() in json.loads(class_info.days_of_week):
        args = [img_path, app_path]
        begin = map(int, begin.split(":"))
        end = map(int, end.split(":"))
        start = today.replace(hour=begin[0], minute=(begin[1] + 59) % 60)
        fin = today.replace(hour=end[0], minute=(end[1] + 59) % 60)
        args = [class_info.class_id] + args
        job_id = '%d-%d' % (class_info.class_id, int(time.mktime(date(today.year, today.month, today.day).timetuple())))
        add_job(snapshot_job, args, job_id, start, fin, interval)
    return class_info


def delete_class(class_id):
    ClassInfo.query.filter_by(class_id=class_id).delete()
    CountInfo.query.filter_by(class_id=class_id).delete()
    Message.query.filter_by(class_id=class_id).delete()
    db.session.commit()
    today = datetime.today()
    job_id = '%d-%d' % (class_id, int(time.mktime(date(today.year, today.month, today.day).timetuple())))
    scheduler.get_job(job_id).remove()


def query_class(name=None, days_of_week=None, creator=None, page=1, per_page=PER_PAGE):
    query = ClassInfo.query
    if name is not None:
        query = query.filter(ClassInfo.name.like("%%%s%%" % name))
    if days_of_week is not None:
        query = query.filter_by(days_of_week=json.dumps(days_of_week))
    if creator is not None:
        query = query.filter_by(creator=creator)
    return query.paginate(page=page, per_page=per_page)


def query_counts(begin=None, end=None, class_id=None, name=None, last=None, page=1, per_page=PER_PAGE):
    query = CountInfo.query
    result = {'total': 0, 'data': []}
    if name:
        query = query.filter(CountInfo.name.like("%%%s%%" % name))
    if class_id:
        query = query.filter_by(class_id=class_id)
        if last:
            min_query = query
            all_counts = min_query.order_by(CountInfo.taken_at.desc()).all()
            if len(all_counts) == 0:
                counts = query.order_by(CountInfo.count_id.desc()).all()
                result['total'] = len(counts)
                result['data'] = counts
                return result
            mins = [datetime.min] * last
            min_ = datetime.max
            for item in all_counts:
                taken = datetime.strptime(item.taken_at.strftime("%Y-%m-%d"), "%Y-%m-%d")
                change = False
                if taken > mins[0]:
                    taken, mins[0] = mins[0], taken
                    change = True
                if taken > mins[1]:
                    taken, mins[1] = mins[1], taken
                    change = True
                if taken > mins[2]:
                    taken, mins[2] = mins[2], taken
                    change = True
                if change and item.taken_at < min_:
                    min_ = item.taken_at
            query = query.filter(CountInfo.taken_at >= min_)
    if begin is not None:
        query = query.filter(CountInfo.taken_at >= datetime.fromtimestamp(begin))
    if end is not None:
        query = query.filter(CountInfo.taken_at < datetime.fromtimestamp(begin))
    if per_page == -1:
        counts = query.order_by(CountInfo.count_id.desc()).all()
        result['total'] = len(counts)
        result['data'] = counts
    else:
        counts = query.order_by(CountInfo.count_id.desc()).paginate(page=page, per_page=per_page)
        result['total'] = counts.total
        result['data'] = counts.items
    return result


def schedule_class():
    query = ClassInfo.query
    today = datetime.today().weekday()
    query = query.filter(ClassInfo.days_of_week.contains(str(today)))
    return query.all()


def snapshot_job(args):
    if not db.app and not db.engine:
        db.app = scheduler.app
        db.init_app(scheduler.app)
    with app.app_context():
        app.logger.debug("snap job run for %s" % time.asctime(datetime.now().timetuple()))
    snapshot(args[0], args[1], args[2])


def add_daily_job(args):
    db.app = scheduler.app
    db.init_app(scheduler.app)
    class_list = schedule_class()
    today = datetime.today()
    for item in class_list:
        begin = map(int, item.begin.split(":"))
        end = map(int, item.end.split(":"))
        start = today.replace(hour=begin[0], minute=(begin[1] + 59) % 60)
        fin = today.replace(hour=end[0], minute=(end[1] + 59) % 60)
        snap_args = [item.class_id] + args
        job_id = '%d-%d' % (item.class_id, int(time.mktime(date(today.year, today.month, today.day).timetuple())))
        if scheduler.get_job(job_id) is not None:
            add_job(snapshot_job, snap_args, job_id, start, fin, item.interval)


def add_job(job, args, job_id, start_date=None, end_date=None, interval=5):
    if end_date < datetime.now():
        scheduler.app.logger.info("end")
        return
    scheduler.app.logger.debug("add job %s" % job_id)
    scheduler.app.logger.debug("args length %d" % len(args))
    _job_ = scheduler.get_job(job_id)
    if _job_:
        _job_.modify(minutes=interval, start_date=start_date, end_date=end_date)
    else:
        if INTERVAL == 'm':
            scheduler.add_job(job, 'interval', args=[args], id=job_id, minutes=interval, start_date=start_date,
                              end_date=end_date, coalesce=False, misfire_grace_time=1)
        elif INTERVAL == 's':
            scheduler.add_job(job, 'interval', args=[args], id=job_id, seconds=interval, start_date=start_date,
                              end_date=end_date, coalesce=False, misfire_grace_time=1)
            # scheduler.add_job(job, 'date', args=[args], run_date=datetime(2016, 12, 14, 17, 28, 30))


def add_msg(user, msg_type, extra, class_id):
    msg = Message(msg_type, extra, user, class_id)
    db.session.add(msg)
    db.session.flush()
    db.session.commit()


def get_msgs(user):
    msgs = Message.query.filter_by(msg_to=user).all()
    return msgs


def read_msgs(user):
    msgs = get_msgs(user)
    clear_msg(user)
    return msgs


def clear_msg(user):
    Message.query.filter_by(msg_to=user).delete()
    db.session.commit()


def broadcast(class_info, count_info):
    kwargs = {'event': SNAPSHOT, 'data': SNAPSHOT_NEW, 'msg': 'new snapshot comes', 'namespace': REFRESH_NOTIFICATION}
    # kwargs = {'event': SNAPSHOT, 'data': SNAPSHOT_NEW, 'msg': 'new snapshot comes',
    # 'room': 'class %d' % class_info.class_id, 'namespace' ; REFRESH_NOTIFICATION}
    eventlet.spawn(notify, **kwargs)
    kwargs.clear()
    count = count_info.count
    warning = class_info.total * class_info.warning
    if warning > count * 100:
        warn_msg = u"课程 %s 中 参与人数 %d 少于目标人数 %d x %d%%" % (
            class_info.name.encode(), count, class_info.total, class_info.warning)
        add_msg(class_info.creator, WARN_LEVEL, warn_msg, count_info.class_id)
        # kwargs = {'msg': warn_msg, 'room': 'user %d' % class_info.creator}
        kwargs = {'msg': warn_msg}
        eventlet.spawn(notify, **kwargs)


def notify(data=WARN_LEVEL, msg=None, event=WARN_EVENT, namespace=DEFAULT_NOTIFICATION, room=None):
    with app.app_context():
        content = {'msg': msg, 'data': data}
        if room:
            emit(event, content, namespace=namespace, room=room, callback=finish)
        else:
            emit(event, content, namespace=namespace, broadcast=True, callback=finish)


def finish():
    # app.logger.info('notify success')
    pass
