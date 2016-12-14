# -*- coding: utf-8 -*-
from datetime import datetime

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler

from utils import SCHEDULER_DB

scheduler = APScheduler()


class Config(object):
    JOBS = [
        {
            'id': 'job' + str(datetime.now()),
            'func': 'guozijian.flask_scheduler:job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SCHEDULER_DB)
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 10}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False
    }

    SCHEDULER_API_ENABLED = True


def job1(a, b):
    print(str(a) + ' ' + str(b))
    scheduler.app.logger.info("test")
