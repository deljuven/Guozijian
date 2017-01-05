# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask_bootstrap import Bootstrap
from flask_user import LoginManager
from sqlalchemy.exc import IntegrityError

from database import db
from scheduler import init_scheduler, scheduler, add_daily_scheduler
from service import add_daily_job
from app import app, APP_PATH, APP_IMG_SAV_PATH

bootstrap = Bootstrap(app)

app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
import guozijian.models

with app.app_context():
    try:
        db.create_all()
        date = datetime.strptime('2016-12-05 05:45:06', "%Y-%m-%d %H:%M:%S")
        init_count = models.CountInfo('803442272850210816.jpg', 'static\\data\\img\\803442272850210816.jpg', date, 8)
        user = models.User("test", "test", "test")
        db.session.add(user)
        db.session.add(init_count)
        db.session.flush()
        db.session.commit()
    except IntegrityError as ex:
        app.logger.info(ex.message)

import guozijian.views

# from flask_scheduler import Config, scheduler
# app.config.from_object(Config())
# scheduler.init_app(app)
# scheduler.start()
if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    init_scheduler(app)
    add_daily_scheduler(add_daily_job, APP_IMG_SAV_PATH, APP_PATH)
    add_daily_job([APP_IMG_SAV_PATH, APP_PATH])
    scheduler.start()

