# -*- coding: utf-8 -*-
from flask_script import Manager
from guozijian import app

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
