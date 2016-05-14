# coding: utf8

from crawler.eastmoney.quote_realtime import fetch_stock_quote

quote = fetch_stock_quote('600597')
for k,v in quote.iteritems():
    print k, v
