from datetime import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from database import db
from models import Test
from service import schedule_class
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
        'misfire_grace_time': 1
    }
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
    scheduler.app = app


def pong():
    print datetime.now()


def add_daily_scheduler():
    scheduler.add_job(add_daily_job, 'cron', year="*", month="*", day_of_week="1-5", hour="0",
                      minute="5/5", second="0", coalesce=True)


def add_daily_job():
    # job = kwargs['job']
    # query = kwargs['query']
    scheduler.app.logger.info('test')
    db.app = scheduler.app
    db.init_app(scheduler.app)
    test = Test("test" + str(datetime.utcnow()))
    db.session.add(test)
    db.session.flush()
    db.session.commit()
    class_list = schedule_class()
    scheduler.app.logger.info(len(class_list))


def add_job(job, start_date, end_date, interval=5):
    if end_date < datetime.now():
        return
        # scheduler.add_job(job, 'interval', minutes=interval, start_date=max([start_date, datetime.now()]),
        #                   end_date=end_date)
