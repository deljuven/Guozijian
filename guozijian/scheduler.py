# -*- coding: utf-8 -*-
import time
from datetime import date, datetime

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from utils import SCHEDULER_DB
import eventlet
eventlet.monkey_patch()


scheduler = BackgroundScheduler()

scheduler_job_store = SQLAlchemyJobStore(url=SCHEDULER_DB)


def init_scheduler(app):
    jobstores = {
        'default': MemoryJobStore()
    }
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 1}
    }
    job_defaults = {
        'coalesce': False,
        'misfire_grace_time': 1,
        'max_instances ': 1
    }
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    scheduler.app = app
    scheduler._logger = app.logger


def add_daily_scheduler(job, img_path, app_path):
    args = [img_path, app_path]
    misfire = 24 * 60 * 60
    today = datetime.today()
    daily_id = str(int(time.mktime(date(today.year, today.month, today.day).timetuple())))
    scheduler.add_job(job, 'cron', args=[args], id=daily_id, year="*", month="*", day_of_week="1-5", hour="0",
                      minute="5/5", second="0", coalesce=True, misfire_grace_time=misfire)
    # scheduler.add_job(add_daily_job, 'interval', args=args, minutes=1, start_date='2016-12-14 17:10:00',
    #                   end_date='2016-12-14 17:30:00')
