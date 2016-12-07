from datetime import datetime, timedelta

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
    scheduler.add_job(add_daily_job, 'cron', year="*", month="*", day_of_week="1-5", hour="0", minute="0", second="0")


def add_daily_job():
    pass


def add_schedule():
    start_date = datetime.now() + timedelta(seconds=30)
    end_date = datetime.now() + timedelta(seconds=60)
    scheduler.add_job(pong, 'interval', seconds=15, start_date=start_date, end_date=end_date)
