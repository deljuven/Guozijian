# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_user import LoginManager
from sqlalchemy.exc import IntegrityError

from database import db
from models import db
from scheduler import init_scheduler, add_daily_scheduler, scheduler
from utils import DB_URI, SQLITE_URI

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.debug = True;
# app.use_reloader = True;

APP_IMG_SAV_PATH = os.path.join(app.root_path, 'static', 'data', 'img')
APP_PATH = app.root_path
DB_PATH = os.path.join(app.root_path, 'db')

if not os.path.exists(APP_IMG_SAV_PATH):
    os.makedirs(APP_IMG_SAV_PATH)
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

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

# from flask_scheduler import Config, scheduler
# app.config.from_object(Config())
# scheduler.init_app(app)
# scheduler.start()
init_scheduler(app)
add_daily_scheduler(APP_IMG_SAV_PATH)
scheduler.start()

import guozijian.views
