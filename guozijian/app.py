# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_socketio import SocketIO

from utils import SQLITE_URI

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.debug = True;
# app.use_reloader = True;

socketio = SocketIO(app, logger=True)

APP_IMG_SAV_PATH = os.path.join(app.root_path, 'static', 'data', 'img')
APP_PATH = app.root_path
DB_PATH = os.path.join(app.root_path, 'db')

if not os.path.exists(APP_IMG_SAV_PATH):
    os.makedirs(APP_IMG_SAV_PATH)
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

