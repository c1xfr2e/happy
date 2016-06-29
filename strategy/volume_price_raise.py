# coding: utf-8

from datetime import date, timedelta
from sqlalchemy import and_
from models import Session, Quote, Stock

ss = Session()

condition = and_(
    Stock.net_profit_growth > 30,
    Stock.listing_date < date.today() - timedelta(days=15)
    # Stock.market_value < 150 * (10**8)
)
stocks = ss.query(Stock).filter(condition).all()

results = []

for stock in stocks:

    N = 3
    last_n = ss.query(Quote).filter(Quote.code == stock.code).order_by(Quote.datetime.desc()).limit(N).all()
    if not last_n or len(last_n) != N or last_n[0].datetime.date() != date.today():
        continue

    q1, q2, q3 = last_n[2], last_n[1], last_n[0]
    if q1.change > 0 and q2.change > 0 and q3.change > 0 and \
       q1.close < q2.close < q3.close and \
       q1.volume < q2.volume < q3.volume and \
       q1.percent < q2.percent < q3.percent:
        results.append(stock)

for stock in results:
    print stock.code, stock.name
