# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_user import LoginManager

from utils import DB_URI
from scheduler import init_scheduler, add_schedule, scheduler


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.debug = True;
# app.use_reloader = True;

APP_IMG_SAV_PATH= os.path.join(app.instance_path, 'static','data','img')

bootstrap = Bootstrap(app)

app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)

init_scheduler()
add_schedule()
# scheduler.start()

import guozijian.views
import guozijian.models
