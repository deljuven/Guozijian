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


def add_schedule():
    start_date = datetime.now() + timedelta(seconds=30)
    end_date = datetime.now() + timedelta(seconds=60)
    scheduler.add_job(pong, 'interval', seconds=15, start_date=start_date, end_date=end_date)
