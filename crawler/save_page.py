# coding: utf-8

import requests

url = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=sz300342'
r = requests.get(url)
with open('tyjd_.html', 'wb') as f:
    f.write(r.content)
