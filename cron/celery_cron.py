# coding: utf-8

from celery import Celery
from celery.schedules import crontab
from cron import celery_config
from sync.pull_stock import pull_all_stock_profile
from sync.pull_last_quote import pull_last_quote
from models import Session, HSIndex
from db.mongo import client

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
    }
}


@app.task
def pull_stock_profile():
    codes = [_['code'] for _ in client.alchemist.stock_codes.find()]
    pull_all_stock_profile(codes)


@app.task
def pull_close_quote():
    index_code_to_sync = [
        '000001',
        '000003',
        '000016',
        '000300',
        '399001',
        '399006',
        '399102'
    ]

    s = Session()
    for index in s.query(HSIndex).filter(HSIndex.code.in_(index_code_to_sync)).all():
        pull_last_quote(index, True)
