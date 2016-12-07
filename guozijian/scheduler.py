from datetime import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from utils import DB_URI

scheduler = BackgroundScheduler()


def init_scheduler():
    jobstores = {
        'default': SQLAlchemyJobStore(url=DB_URI)
    }
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 10}
    }
    job_defaults = {
        'coalesce': False
    }
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)


def pong():
    print datetime.now()


def add_daily_scheduler():
    scheduler.add_job(add_daily_job, 'cron', year="*", month="*", day_of_week="1-5", hour="0", minute="0", second="0",
                      coalesce=True)


def add_daily_job():
    pass


def add_job(start_date, end_date, interval=5):
    if end_date < datetime.now():
        return
    scheduler.add_job(pong, 'interval', minutes=interval, start_date=max([start_date, datetime.now()]),
                      end_date=end_date)
