# coding: utf-8

from sqlalchemy import and_
import redis
from models import Session, Stock, Quote

r = redis.StrictRedis(host='localhost', port=6379, db=0)

ss = Session()
stocks = ss.query(Stock.market, Stock.code).all()

for stock in stocks:
    key = 'highof20:%s%s' % (stock.market, stock.code)
    existing = r.hmget(key, 'time')
    if existing[0]:
        continue

    quotes = ss.query(Quote).filter(
        and_(Quote.market == stock.market, Quote.code == stock.code, Quote.period == 'd1')
    ).order_by(Quote.datetime.desc()).limit(20).all()

    if not quotes:
        continue

    high_quote = max(quotes, key=lambda q: q.high)

    r.hmset(key, {'time': high_quote.datetime, 'high': high_quote.high})
