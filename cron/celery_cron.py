# coding: utf-8

from datetime import date, timedelta
import logging

from celery import Celery
from celery.schedules import crontab
from sqlalchemy import and_, not_

from cron import celery_config
from sync.pull_stock import update_stock_profile as usp
from sync.pull_last_quote import pull_last_quote
from models import Session, HSIndex, Stock, Quote
from util.date_time import is_trade_day
from quote.merge_quotes import merge_quotes

from config import log_format

logging.getLogger().setLevel(logging.WARNING)
logging.basicConfig(format=log_format)

app = Celery('celery_cron')
app.config_from_object(celery_config)

app.conf.CELERYBEAT_SCHEDULE = {
    'update_stock_profile': {
        'task': 'cron.celery_cron.update_stock_profile',
        'schedule': crontab(day_of_week='mon-fri', hour='15', minute='5')
    },
    'pull_close_quote': {
        'task': 'cron.celery_cron.pull_close_quote',
        'schedule': crontab(day_of_week='mon-fri', hour='16', minute='00')
    },
    'create_this_week_quote': {
        'task': 'cron.celery_cron.create_this_week_quote',
        'schedule': crontab(day_of_week='fri', hour='17', minute='00')
    }
}

'''
    'sync_quotes_5min_1': {
        'task': 'cron.celery_cron.sync_quotes',
        'schedule': crontab(day_of_week='mon-fri', hour='10,13,14', minute='*/5')
    },
    'sync_quotes_5min_2': {
        'task': 'cron.celery_cron.sync_quotes',
        'schedule': crontab(day_of_week='mon-fri', hour='9', minute='20,25,30,35,40,45,50,55')
    },
    'sync_quotes_5min_3': {
        'task': 'cron.celery_cron.sync_quotes',
        'schedule': crontab(day_of_week='mon-fri', hour='11', minute='0,5,10,15,20,25,30')
    },
'''


@app.task
def update_stock_profile():
    if not is_trade_day(date.today()):
        return

    ss = Session()
    to_update = ss.query(Stock.code).filter(
        Stock.update_time < date.today()
    ).distinct().all()

    usp([_.code for _ in to_update])


@app.task
def pull_close_quote():
    if not is_trade_day(date.today()):
        return

    ss = Session()
    for index in ss.query(HSIndex).all():
        quote = pull_last_quote(index, True)
        if quote:
            ss.merge(quote)
            ss.commit()

    updated = ss.query(Quote.code).filter(Quote.datetime >= date.today()).distinct().subquery()
    to_update = ss.query(Stock).filter(
        not_(
            Stock.code.in_(updated)
        )
    ).distinct().all()

    for stock in to_update:
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

    securities = ss.query(Quote.code).distinct().all()
    for sec in securities:
        sec_quotes_of_this_week = ss.query(Quote).filter(
            and_(
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


@app.task
def sync_quotes():
    if not is_trade_day(date.today()):
        return


if __name__ == '__main__':
    pull_stock_profile.apply()
