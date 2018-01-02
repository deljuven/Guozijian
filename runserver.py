# -*- coding: utf-8 -*-
from flask_script import Manager

from finder.app import app

manager = Manager(app)


# def run():
#     socketio.run(app, host="0.0.0.0")


if __name__ == "__main__":
    # run()
    manager.run()
