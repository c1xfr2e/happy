# coding: utf-8

import pickle
from datetime import date

import requests

from history.tldata.config import headers

data = pickle.load(open('../../data/exdiv/600036', 'rb'))


url = 'https://api.wmcloud.com/data/v1/api/market/getMktAdjf.json'
payload = {
    'endDate': date.today().strftime('%Y%m%d'),
    'ticker': '300342'
}

resp = requests.get(url, headers=headers, params=payload)
json_res = resp.json()
data = json_res['data']
pickle.dump(data, open('../../data/exdiv/300342', 'w'))
