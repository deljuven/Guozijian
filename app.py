# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def home():
    return redirect(url_for('index'))


@app.route('/hello')
def hello():
    return render_template("login.html", username='test')


@app.route('/index')
def index():
    return 'Hello World!'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == "__main__":
    manager.run()
