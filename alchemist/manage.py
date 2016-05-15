# coding: utf-8
from __future__ import absolute_import

from flask import Flask
from flask.ext.script import Manager, Shell
from crawler.eastmoney.quote_realtime import fetch_index_quote

app = Flask(__name__)
manager = Manager(app)


@app.route('/sync_index')
def index():
    hq = fetch_index_quote('000001')
    print hq
    return ''


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
