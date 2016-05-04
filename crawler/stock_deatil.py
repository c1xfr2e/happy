# coding: utf-8

import requests
from bs4 import BeautifulSoup
from db import db_conn

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

url = 'http://quote.eastmoney.com/sz300342.html'
r = requests.get(url)
print r.encoding

f = open('../htmls/tyjd_detail.html', 'r')
content = f.read()
text = content.decode('gbk')
soup = BeautifulSoup(text)

datas_text = []
trs = soup.find('table', id='rtp2').find('tbody').find_all('tr')
for tr in trs:
    tds = tr.find_all('td')
    for td in tds:
        datas_text.append(td.text)

datas_dict = {}
for data in datas_text:
    print data.split(u'：')
