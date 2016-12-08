# -*- coding: utf-8 -*-
import os
from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_user import LoginManager
from sqlalchemy.exc import IntegrityError
from werkzeug.wrappers import Request

from scheduler import init_scheduler, add_job, scheduler
from utils import DB_URI, SQLITE_URI


class MethodRewriteMiddleware(object):
    def __init__(self, app, input_name='_method'):
        self.app = app
        self.input_name = input_name

    def __call__(self, environ, start_response):
        request = Request(environ)

        if self.input_name in request.form:
            method = request.form[self.input_name].upper()

            if method in ['GET', 'POST', 'PUT', 'DELETE']:
                environ['REQUEST_METHOD'] = method

        return self.app(environ, start_response)


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)
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

db = SQLAlchemy()
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

init_scheduler()
# add_job()
# scheduler.start()

import guozijian.views
