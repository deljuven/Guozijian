from datetime import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from database import db
from service import schedule_class, snapshot
from utils import SCHEDULER_DB

scheduler = BackgroundScheduler()


def init_scheduler(app):
    jobstores = {
        'default': SQLAlchemyJobStore(url=SCHEDULER_DB)
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


def snapshot_job(args):
    db.app = scheduler.app
    db.init_app(scheduler.app)
    snapshot(args[0], args[1])


def add_daily_scheduler(base_path):
    args = [base_path]
    misfire = 24 * 60 * 60
    scheduler.add_job(add_daily_job, 'cron', args=args, year="*", month="*", day_of_week="1-5", hour="0",
                      minute="5/5", second="0", coalesce=True, misfire_grace_time=misfire)
    # scheduler.add_job(add_daily_job, 'interval', args=args, minutes=1, start_date='2016-12-14 17:10:00',
    #                   end_date='2016-12-14 17:30:00')


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
        args = [item.class_id] + [args]
        add_job(snapshot_job, args, start, fin, item.interval)


def add_job(job, args=None, start_date=None, end_date=None, interval=5):
    if end_date < datetime.now():
        scheduler.app.logger.info("end")
        return
    scheduler.add_job(job, 'interval', args=[args], minutes=interval, start_date=max([start_date, datetime.now()]),
                      end_date=end_date, coalesce=False, misfire_grace_time=1)
    # scheduler.add_job(job, 'date', args=[args], run_date=datetime(2016, 12, 14, 17, 28, 30))
