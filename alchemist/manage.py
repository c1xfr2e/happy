# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime, time

from flask import Flask
from flask.ext.script import Manager, Shell
from crawler.sina_finance.hq_last import hq_last
from models import Session
from models.hq_snapshot import HQSnapshot
from crawler import util
from indicator.basic import change_percent


app = Flask(__name__)
manager = Manager(app)


@app.route('/synchq/<code>')
def sync_hq(code):
    code = '399006'


@app.route('/sync')
def index():
    index_codes = [
        '000001', '399102', '399006', '000300'
    ]
    for code in index_codes:
        market = util.index_market(code)
        hq = hq_last(market, code)

        now = datetime.now()
        this_date = date(now.year, now.month, now.day)
        this_minute = time(now.hour, now.minute, 0)

        change = hq['price'] - hq['pre_close']
        change_pct = change_percent(hq['price'], hq['pre_close'])

        snapshot = HQSnapshot(
            market=market,
            code=code,
            name=hq['name'],
            date=this_date,
            time=this_minute,
            price=hq['price'],
            pre_close=hq['pre_close'],
            open=hq['open'],
            low=hq['low'],
            high=hq['high'],
            change=change,
            percent=change_pct,
            volume=hq['volume'],
            money=hq['volume_money']
        )

        session = Session()
        session.merge(snapshot)
        session.commit()

        print 'sync: ', code

    return 'ok'


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
