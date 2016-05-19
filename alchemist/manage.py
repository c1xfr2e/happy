# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime, time

from flask import Flask
from flask.ext.script import Manager, Shell
from crawler.eastmoney.quote_realtime import fetch_index_quote, fetch_stock_quote
from crawler.sina_finance.hq_last import hq_last
from models import Session
from models.hq_snapshot import HQSnapshot


app = Flask(__name__)
manager = Manager(app)


@app.route('/synchq/<code>')
def sync_hq(code):
    code = '399006'


@app.route('/sync')
def index():
    code = '399102'
    hq = hq_last('sz', code)

    '''
        for k, v in hq.iteritems():
        print k, v
    '''

    now = datetime.now()
    this_date = date(now.year, now.month, now.day)
    this_minute = time(now.hour, now.minute, 0)

    snapshot = HQSnapshot(
        code=code,
        name=hq['name'],
        date=hq['date'],
        time=hq['time'],
        price=hq['price'],
        pre_close=hq['pre_close'],
        open=hq['open'],
        low=hq['low'],
        high=hq['high'],
        volume=hq['volume'],
        volume_money=hq['volume_money']
    )

    session = Session()
    session.merge(snapshot)
    session.commit()

    return str(hq)


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
