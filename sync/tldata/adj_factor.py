# coding: utf-8

from datetime import date, time
import requests
from sync.tldata.config import headers


url = 'https://api.wmcloud.com/data/v1/api/market/getMktAdjf.json'
payload = {
    'endDate': date(2016, 6, 15).strftime('%Y%m%d'),
    'ticker': '601377'
}

resp = requests.get(url, headers=headers, params=payload)
json_res = resp.json()
for data in json_res['data']:
    print data['exDivDate'], data['adjFactor']

