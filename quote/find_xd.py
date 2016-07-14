# coding: utf-8

from sqlalchemy import and_
from sqlalchemy.sql import func

from models import Session, HSIndex, Quote
from crawler.tjqka.hq_last import hq_last

ss = Session()

lastest_datetime = ss.query(Quote.code, func.max(Quote.datetime).label('datetime'))\
    .filter(Quote.period == 'd1').group_by(Quote.code)\
    .subquery()

lastest_quotes = ss.query(Quote, lastest_datetime).filter(and_(
    Quote.period == 'd1',
    Quote.code == lastest_datetime.c.code,
    Quote.datetime == lastest_datetime.c.datetime
))

indexs = ss.query(HSIndex.market, HSIndex.code).all()

xd_list = []

for result in lastest_quotes:
    quote = result[0]
    if quote.code in indexs:
        continue
    market = 'sh' if quote.code[0] == '6' else 'sz'
    last = hq_last(market, quote.code, False)
    if 'close' in last and last['close'] != quote.close:
        xd_list.append({
            'code': quote.code,
            'old': quote.close,
            'new': last['close']
        })

print xd_list
