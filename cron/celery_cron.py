# coding: utf-8

from celery import Celery
from celery.schedules import crontab
from cron import celery_config
from sync.pull_stock import pull_all_stock_profile
from sync.pull_index_hq_daily import pull_index_last_hq
from models import Session, HSIndex

app = Celery('celery_cron')
app.config_from_object(celery_config)

app.conf.CELERYBEAT_SCHEDULE = {
    'pull_today_quote': {
        'task': 'cron.celery_cron.pull_today_quote',
        'schedule': crontab(day_of_week='mon-fri', hour='15', minute='30')
    }
}


@app.task
def pull_today_quote():
    s = Session()
    for index in s.query(HSIndex).all():
        pull_index_last_hq(index)
