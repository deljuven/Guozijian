# -*- coding: utf-8 -*-
import os

from flask import Flask

from utils import SQLITE_URI

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.debug = True;
# app.use_reloader = True;

APP_PATH = app.root_path
APP_IMG_SAV_PATH = os.path.join(APP_PATH, 'static', 'data', 'img')
DB_PATH = os.path.join(APP_PATH, 'db')
app.config['UPLOADED_PHOTOS_DEST'] = APP_IMG_SAV_PATH

if not os.path.exists(APP_IMG_SAV_PATH):
    os.makedirs(APP_IMG_SAV_PATH)
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

