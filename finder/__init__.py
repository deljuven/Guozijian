# -*- coding: utf-8 -*-
from datetime import datetime

from flask_bootstrap import Bootstrap
from sqlalchemy.exc import IntegrityError

from app import app, APP_PATH, APP_IMG_SAV_PATH
from database import db
from login import login_manager

bootstrap = Bootstrap(app)

login_manager.init_app(app)

db.init_app(app)
import finder.models

with app.app_context():
    try:
        db.create_all()
        date = datetime.strptime('2016-12-05 05:45:06', "%Y-%m-%d %H:%M:%S")
        user = models.User("test", "test", "test")
        db.session.add(user)
        db.session.flush()
        db.session.commit()
    except IntegrityError as ex:
        app.logger.info(ex.message)

import finder.views
