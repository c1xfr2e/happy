# coding: utf8

from crawler.eastmoney.quote_realtime import fetch_index_quote, fetch_stock_quote

quote = fetch_index_quote('000001')
for k,v in quote.iteritems():
    print k, v
