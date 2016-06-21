# coding: utf-8

from datetime import date
from collections import defaultdict

from models import Session, Quote, Stock

ss = Session()
stocks = ss.query(Stock).all()

n_green = defaultdict(list)

for stock in stocks:
    N = 7
    last_n = ss.query(Quote).filter(Quote.code == stock.code).order_by(Quote.datetime.desc()).limit(N).all()
    if not last_n or last_n[0].datetime.date() != date.today():
        continue

    count = 0
    for q in last_n:
        width = q.high - q.low
        if width == 0:
            continue
        if q.change < 0 and q.close - q.open < 0:
            count += 1
        else:
            break

    if count < 3:
        continue

    last = last_n[0]
    width = last.high - last.low
    if width == 0:
        continue
    delta = last.close - last.open
    p = delta / width * 100
    if -10 < p < 10:
        n_green[count].append(stock)

for n, stocks in n_green.iteritems():
    print n
    for s in stocks:
        print s.code, s.name
