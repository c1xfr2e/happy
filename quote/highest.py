# coding: utf-8

from datetime import date

from sqlalchemy import and_
import redis
from models import Session, Stock, Quote

r = redis.StrictRedis(host='localhost', port=6379, db=0)

ss = Session()
stocks = ss.query(Stock.market, Stock.code).all()

for stock in stocks:
    quotes = ss.query(Quote).filter(
        and_(Quote.market == stock.market, Quote.code == stock.code, Quote.period == 'd1')
    ).order_by(Quote.datetime.desc()).limit(20).all()

    if not quotes:
        continue

    high_quote = max(quotes, key=lambda q: q.high)

    key = 'highof20:%s%s' % (stock.market, stock.code)
    r.hmset(key, {'time': high_quote.datetime, 'high': high_quote.high})

    if high_quote.datetime == date.today():
        print high_quote.name, high_quote.code
