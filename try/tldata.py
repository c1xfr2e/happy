# coding: utf-8

import requests

from datetime import date
from history.tldata.quotes import get_history_quotes

quotes = get_history_quotes(
    date(1991, 11, 10),
    date(2001, 1, 1),
    '600000'
)

token = '27f1ef056e9a5cfdfe3cee5d1c0779e59db0125fc6416010c363d195c10dfdf6'
url = 'https://api.wmcloud.com/data/v1/api/market/getMktEqudAdj.json'

headers = {
    'Authorization': "Bearer " + token,
    'Accept-Encoding': 'gzip, deflate'
}
payload = {
    'field': '',
    'beginDate': '19991110',
    'endDate': '20160601',
    'secID': '',
    'ticker': '300342',
    'tradeDate': ''
}

r = requests.get(url, headers=headers, params=payload)
print(r.url)
print(r.json())

data = r.json()['data'][1]
for k, v in data.iteritems():
    print k, v
