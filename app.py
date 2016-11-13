# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('index'))


@app.route('/hello')
def hello():
    return render_template("hello.html", username = 'test')


@app.route('/index')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
