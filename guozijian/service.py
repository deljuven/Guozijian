# -*- coding: utf-8 -*-
import json
import os
import time
from datetime import datetime, date

from database import db
from face.ImageDetector import ImageDetector
from models import CountInfo, ClassInfo, Test
from scheduler import scheduler
from utils import PER_PAGE, RETRY
from video.VideoService import VideoService, VideoException


def snapshot(class_id, img_path, app_path):
    vs = VideoService()
    try:
        url = vs.take_picture(RETRY)
    except VideoException as e:
        return {'success': False, 'err': e.message}
    detector = ImageDetector(url, img_path)
    faces = detector.detect(4)
    save_to_db(detector, faces, class_id, app_path)
    return {'success': True}


def save_to_db(detector, face_count, class_id, app_path):
    name = os.path.basename(detector.file_path)
    path = os.path.relpath(detector.file_path, app_path)
    count = CountInfo(name, path, datetime.now(), face_count, class_id)
    db.session.add(count)
    db.session.flush()
    db.session.commit()


def add_class(name, begin, end, days_of_week, total, img_path, app_path, interval=5):
    class_info = ClassInfo(name, begin, end, days_of_week, total, interval)
    db.session.add(class_info)
    db.session.flush()
    db.session.commit()
    today = datetime.today()
    if today.weekday() in json.loads(class_info.days_of_week):
        args = [img_path, app_path]
        begin = map(int, begin.split(":"))
        end = map(int, end.split(":"))
        start = today.replace(hour=begin[0], minute=(begin[1] + 59) % 60)
        fin = today.replace(hour=end[0], minute=(end[1] + 59) % 60)
        args = [class_info.class_id] + [args]
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
        args = [class_info.class_id] + [args]
        job_id = '%d-%d' % (class_info.class_id, int(time.mktime(date(today.year, today.month, today.day).timetuple())))
        add_job(snapshot_job, args, job_id, start, fin, interval)
    return class_info


def delete_class(class_id):
    ClassInfo.query.filter_by(class_id=class_id).delete()
    CountInfo.query.filter_by(class_id=class_id).delete()
    db.session.commit()


def query_class(name=None, days_of_week=None, page=1, per_page=PER_PAGE):
    query = ClassInfo.query
    if name is not None:
        query = query.filter(ClassInfo.name.like("%%%s%%" % name))
    if days_of_week is not None:
        query = query.filter_by(days_of_week=json.dumps(days_of_week))
    return query.paginate(page=page, per_page=per_page)


def query_counts(begin=None, end=None, class_id=None, name=None, page=1, per_page=PER_PAGE):
    query = CountInfo.query
    if name:
        query = query.filter(CountInfo.name.like("%%%s%%" % name))
    if class_id:
        query = query.filter_by(class_id=class_id)
    if begin is not None:
        query = query.filter(CountInfo.taken_at >= datetime.fromtimestamp(begin))
    if end is not None:
        query = query.filter(CountInfo.taken_at < datetime.fromtimestamp(begin))
    if page == -1 and per_page == -1:
        return query.all()
    return query.paginate(page=page, per_page=per_page)


def pong(class_id, start, finish):
    test = Test(name="test_" + class_id)
    print start, finish
    db.session.add(test)
    db.session.flush()
    db.session.commit()


def schedule_class():
    query = ClassInfo.query
    today = datetime.today().weekday()
    query = query.filter(ClassInfo.days_of_week.contains(str(today)))
    return query.all()


def snapshot_job(args):
    if not db.app and not db.engine:
        db.app = scheduler.app
        db.init_app(scheduler.app)
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
        add_job(snapshot_job, snap_args, job_id, start, fin, item.interval)


def add_job(job, args, job_id, start_date=None, end_date=None, interval=5):
    if end_date < datetime.now():
        scheduler.app.logger.info("end")
        return
    if scheduler.get_job(job_id):
        return
    scheduler.add_job(job, 'interval', args=[args], id=job_id, minutes=interval, start_date=start_date,
                      end_date=end_date, coalesce=False, misfire_grace_time=1)
    # scheduler.add_job(job, 'date', args=[args], run_date=datetime(2016, 12, 14, 17, 28, 30))
