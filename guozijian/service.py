# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from face.ImageDetector import ImageDetector
from guozijian import db, APP_PATH
from models import CountInfo, ClassInfo
from video.VideoService import VideoService


def test_db():
    if db.session.query("1").from_statement("SELECT 1").all():
        return 'It works.'
    else:
        return 'Something is broken.'


def snapshot():
    vs = VideoService()
    url = vs.take_picture()
    detector = ImageDetector(url)
    faces = detector.detect(4)
    save_to_db(detector, faces)


def save_to_db(detector, face_count):
    name = os.path.basename(detector.file_path)
    path = os.path.relpath(detector.file_path, APP_PATH)
    count = CountInfo(name, path, datetime.now(), face_count)
    db.session.add(count)
    db.session.flush()
    db.session.commit()


def add_class(name, begin, end, days_of_week, total):
    class_info = ClassInfo(name, begin, end, days_of_week, total)
    db.session.add(class_info)
    db.session.flush()
    db.session.commit()
    return class_info


def update_class(id__, name, begin, end, days_of_week, total):
    class_info = ClassInfo.query.get(id__).update(
        dict(name=name, begin=begin, end=end, days_of_week=days_of_week, total=total))
    db.session.commit()
    return class_info


def delete_class(id__):
    ClassInfo.query.get(id__).delete()
    db.session.commit()


def query_class(name=None, days_of_week=None):
    query = ClassInfo.query
    if name is not None:
        query = query.filter(name=name)
    if days_of_week is not None:
        query = query.filter(days_of_week=json.dumps(days_of_week))
    return query.all()
