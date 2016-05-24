# coding: utf-8

"""
Run worker: celery worker -A sync.celery_sample --loglevel=info
Run beat: celery beat -A sync.celery_sample --loglevel=info
"""

from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from . import celery_config

app = Celery('celery_sample')  # broker='redis://localhost', backend='redis://localhost'
app.config_from_object(celery_config)

app.conf.CELERYBEAT_SCHEDULE = {
    'say-hello': {
        'task': 'sync.celery_sample.test',
        'schedule': crontab(minute='*'),
        'args': ('hello',)
    }
}


@app.task
def test(arg):
    print arg


@app.task
def add(x, y):
    return x + y


@app.task
def sub(x, y):
    return x - y
