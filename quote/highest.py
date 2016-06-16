# coding: utf-8

from datetime import date, datetime

from sqlalchemy import and_
import redis
from models import Session, Stock, Quote

r = redis.StrictRedis(host='localhost', port=6379, db=0)
ss = Session()


def create_high_20():
    stocks = ss.query(Stock.code).all()

    for stock in stocks:
        quotes = ss.query(Quote).filter(
            and_(
                Quote.code == stock.code,
                Quote.period == 'd1'
            )
        ).order_by(Quote.datetime.desc()).limit(20).all()

        if not quotes:
            continue

        high_quote = max(quotes, key=lambda q: q.high)

        key = 'highof20:%s%s' % (stock.market, stock.code)
        r.hmset(key, {'time': high_quote.datetime, 'high': high_quote.high})

        if high_quote.datetime == date.today():
            print high_quote.name, high_quote.code


def find_high_at_today():
    close_eq_high = ss.query(Quote.code).filter(
        and_(Quote.datetime == date.today(), Quote.close == Quote.high)
    ).all()
    close_eq_high = [_[0] for _ in close_eq_high]

    min_date = date(2016, 5, 13)

    stocks = ss.query(Stock).filter(Stock.listing_date < min_date).all()
    for stock in stocks:
        key = 'highof20:%s%s' % (stock.market, stock.code)
        high_time = r.hmget(key, 'time')
        if high_time[0] is None:
            continue
        high_date = datetime.strptime(high_time[0], '%Y-%m-%d %H:%M:%S').date()
        if high_date == date.today() and stock.code in close_eq_high:
            print stock.code, stock.name


if __name__ == '__main__':
    find_high_at_today()
