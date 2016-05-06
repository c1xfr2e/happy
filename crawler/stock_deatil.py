# coding: utf-8

import requests
from bs4 import BeautifulSoup
from db import db_conn
from text_util import text_to_number

'''
cursor = db_conn.cursor()
sql = 'select * from hs_ticker'
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for r in results:
        print r[0]
except Exception as e:
    print 'select error', e
'''

url = 'http://quote.eastmoney.com/sh600309.html'
r = requests.get(url)
soup = BeautifulSoup(r.content.decode('gbk'))

'''
收益(一) 0.210
PE(动) 18.74
净资产 5.355
市净率 2.94
收入 53.00亿
同比 16.85%
净利润 4.44亿
同比 -5.78%
毛利率 27.00%
净利率 10.28%
ROE 3.76%
负债率 69.54%
总股本 21.62亿
总值 340.4亿
流通股 21.62亿
流值 340.4亿
每股未分配利润 3.402元
上市时间 2001-01-05
'''

texts = []
trs = soup.find('table', id='rtp2').find('tbody').find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    for td in tds:
        texts.append(td.text.split(u'：'))

datas = {_[0]: _[1] for _ in texts}
for k, v in datas.iteritems():
    print k, v

eps = datas.get(u'收益(一)', None)
if eps is None:
    eps = datas.get(u'收益')
eps = float(eps)
pe = float(datas.get(u'PE(动)', 0))
net_asset_value_per_share = float(datas.get(u'净资产', u'0'))
pb = text_to_number(datas.get(u'净利率', u'0'))
revenue = text_to_number(datas.get(u'收入', u'0'))
revenue_growth = text_to_number(texts[5][1])
net_income = text_to_number(datas.get(u'净利润', u'0'))
net_income_growth = text_to_number(texts[7][1])
roe = text_to_number(datas.get(u'ROE', u'0.0'))
shares_outstanding = text_to_number(datas.get(u'总股本', u'0'))
shares_tradable = text_to_number(datas.get(u'总股本', u'0'))
retained_earnings_per_share = text_to_number(datas.get(u'每股未分配利润', u'0'))
listing_date = datas.get(u'上市时间')

print eps, pe, net_asset_value_per_share, pb, revenue, revenue_growth, net_income,\
      net_income_growth, roe, shares_outstanding, shares_tradable,\
      retained_earnings_per_share, listing_date
