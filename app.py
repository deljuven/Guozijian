# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for

from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def home():
    return redirect(url_for('index'))


@app.route('/hello')
def hello():
    return render_template("guozijian/login.html", username='test')


@app.route('/index')
def index():
    return 'Hello World!'


if __name__ == "__main__":
    app.run(debug=True)
