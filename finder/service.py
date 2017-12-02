# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from database import db
from models import CountInfo, ClassInfo, Message
from utils import PER_PAGE


def snapshot(class_id, img_path, app_path):
    pass


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
    return class_info


def delete_class(class_id):
    ClassInfo.query.filter_by(class_id=class_id).delete()
    CountInfo.query.filter_by(class_id=class_id).delete()
    Message.query.filter_by(class_id=class_id).delete()
    db.session.commit()
    today = datetime.today()


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


def finish():
    # app.logger.info('notify success')
    pass
