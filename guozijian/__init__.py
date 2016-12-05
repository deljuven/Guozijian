# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_user import LoginManager

from scheduler import init_scheduler, add_schedule, scheduler
from utils import DB_URI, SQLITE_URI

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.debug = True;
# app.use_reloader = True;

APP_IMG_SAV_PATH = os.path.join(app.instance_path, 'static', 'data', 'img')

bootstrap = Bootstrap(app)

app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)
import guozijian.models

with app.app_context():
    db.drop_all()
    db.create_all()
    date = datetime.strptime('2016-12-05 05:45:06', "%Y-%m-%d %H:%M:%S")
    init_count = models.CountInfo('803442272850210816.jpg', 'static\\data\\img\\803442272850210816.jpg', date, 8)
    user = models.User("test", "test", "test")
    db.session.add(user)
    db.session.add(init_count)
    db.session.flush()
    db.session.commit()

init_scheduler()
add_schedule()
# scheduler.start()

import guozijian.views
