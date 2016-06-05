# coding: utf-8

import logging
import requests
from datetime import date, time
from itertools import takewhile

from models import Quote, Session
from indicator.basic import change_percent


def create_week_quotes(code):
    sess = Session()
    quotes = sess.query(Quote).filter(code == code).order_by(Quote.from_date).all()
    quotes_in_week = takewhile

def week_quote_from_day():
    pass
