# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from database import db
from face.ImageDetector import ImageDetector
from models import CountInfo, ClassInfo, Test
from utils import PER_PAGE
from video.VideoService import VideoService


def snapshot(class_id, base_path):
    vs = VideoService()
    url = vs.take_picture()
    detector = ImageDetector(url, base_path)
    faces = detector.detect(4)
    save_to_db(detector, faces, class_id, base_path)


def save_to_db(detector, face_count, class_id, base_path):
    name = os.path.basename(detector.file_path)
    path = os.path.relpath(detector.file_path, base_path)
    count = CountInfo(name, path, datetime.now(), face_count, class_id)
    db.session.add(count)
    db.session.flush()
    db.session.commit()


def add_class(name, begin, end, days_of_week, total, interval=5):
    class_info = ClassInfo(name, begin, end, days_of_week, total, interval)
    db.session.add(class_info)
    db.session.flush()
    db.session.commit()
    return class_info


def update_class(class_id, name, begin, end, days_of_week, total, interval):
    class_info = ClassInfo.query.get(class_id)
    class_info.name = name
    class_info.begin = begin
    class_info.end = end
    class_info.days_of_week = json.dumps(days_of_week)
    class_info.total = total
    class_info.interval = interval
    db.session.commit()
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
