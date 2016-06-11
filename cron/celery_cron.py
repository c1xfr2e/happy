# coding: utf-8

from datetime import datetime, date, timedelta
import logging

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import and_

from cron import celery_config
from sync.pull_stock import pull_stock_profile as psp
from sync.pull_last_quote import pull_last_quote
from models import Session, HSIndex, Stock, Quote
from db.mongo import client
from util.date_time import is_trade_day
from quote.create_week_month_quote import merge_quotes

from config import log_format

logging.getLogger().setLevel(logging.WARNING)
logging.basicConfig(format=log_format)

app = Celery('celery_cron')
app.config_from_object(celery_config)

app.conf.CELERYBEAT_SCHEDULE = {
    'pull_stock_profile': {
        'task': 'cron.celery_cron.pull_stock_profile',
        'schedule': crontab(day_of_week='mon-fri', hour='15', minute='5')
    },
    'pull_close_quote': {
        'task': 'cron.celery_cron.pull_close_quote',
        'schedule': crontab(day_of_week='mon-fri', hour='16', minute='30')
    },
    'create_this_week_quote': {
        'task': 'cron.celery_cron.create_this_week_quote',
        'schedule': crontab(day_of_week='fri', hour='17', minute='00')
    }

}


@app.task
def pull_stock_profile():
    if not is_trade_day(date.today()):
        return

    codes = [_['code'] for _ in client.alchemist.stock_codes.find()]
    psp(codes)


@app.task
def pull_close_quote():
    if not is_trade_day(date.today()):
        return

    ss = Session()
    for index in ss.query(HSIndex).all():
        quote = pull_last_quote(index, True)
        if quote:
            ss.add(quote)
            ss.commit()

    stocks = ss.query(Stock).filter(Stock.status == 'L').all()
    for stock in stocks:
        quote = pull_last_quote(stock, False)
        if quote:
            ss.add(quote)
            ss.commit()


@app.task
def create_this_week_quote():
    if not is_trade_day(date.today()):
        return

    ss = Session()

    today = date.today()
    week_first_date = today - timedelta(days=today.weekday())

    securities = ss.query(Quote.market, Quote.code).distinct().all()
    for sec in securities:
        sec_quotes_of_this_week = ss.query(Quote).filter(
            and_(
                Quote.market == sec.market,
                Quote.code == sec.code,
                Quote.datetime >= week_first_date,
                Quote.datetime <= today,
                Quote.period == 'd1'
            )
        ).all()

        if not sec_quotes_of_this_week:
            continue

        week_quote = merge_quotes(sec_quotes_of_this_week)
        week_quote.period = 'w1'
        ss.merge(week_quote)
        ss.commit()


if __name__ == '__main__':
    f = create_this_week_quote
    f.apply()
