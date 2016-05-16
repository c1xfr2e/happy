# coding: utf-8
from __future__ import absolute_import

from flask import Flask
from flask.ext.script import Manager, Shell
from crawler.eastmoney.quote_realtime import fetch_index_quote, fetch_stock_quote
from crawler.sina_finance.hq import hq_snapshot

app = Flask(__name__)
manager = Manager(app)


@app.route('/sync_index')
def index():
    hq = hq_snapshot('sz', '399006')
    for k, v in hq.iteritems():
        print k, v
    return ''


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
