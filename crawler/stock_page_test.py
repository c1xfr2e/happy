# coding: utf-8

import requests
from collections import defaultdict
import logging


logging.getLogger().setLevel(logging.DEBUG)

hs_ticker_prefix = [
    '600', '601', '000', '002', '300'
]


def ticker_permutation():
    tickers = []
    for prefix in hs_ticker_prefix:
        for i in range(0, 1000):
            tickers.append(prefix + '{0:0>3}'.format(i))
    return tickers

candidate_tickers = ticker_permutation()
print len(candidate_tickers)

url_format = 'http://quote.eastmoney.com/{sh_or_sz}{ticker}.html'

valid_tickers = []
status_code_count = defaultdict(lambda: 0)

for ticker in candidate_tickers:
    sh_or_sz = 'sh' if ticker.startswith('6') else 'sz'
    url = url_format.format(sh_or_sz=sh_or_sz, ticker=ticker)
    r = requests.head(url)
    logging.info(url + ' ' + str(r.status_code))
    status_code_count[r.status_code] += 1
    if r.status_code == 200:
        valid_tickers.append(ticker)

logging.info(status_code_count)


import MySQLdb
db = MySQLdb.connect(
    host='rdsbi4u1v33wc6zn0w71o.mysql.rds.aliyuncs.com',
    user='zh', passwd='000000', db='alchemist'
)
cursor = db.cursor()
for ticker in valid_tickers:
    cursor.execute('insert into ticker values("%s")' % ticker)
db.commit()
db.close()
