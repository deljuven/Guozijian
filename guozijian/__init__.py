# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_user import LoginManager

DB_URI = 'mysql+pymysql://mysql:ef5793f4772cfe5a@202.120.40.20:11266/guozijian'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.debug = True;
# app.use_reloader = True;

bootstrap = Bootstrap(app)

app.secret_key = 's3cr3t'
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)

import guozijian.views
import guozijian.models
