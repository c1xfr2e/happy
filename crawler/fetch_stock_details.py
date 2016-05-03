# coding: utf-8

import requests

url_shareholders = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=sz300342'
url_stock_detail = 'http://quote.eastmoney.com/sz300342.html'
r = requests.get(url_stock_detail)
with open('../htmls/tyjd_detail.html', 'wb') as f:
    f.write(r.content)
