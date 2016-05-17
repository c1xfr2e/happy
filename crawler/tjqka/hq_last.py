# coding: utf-8

import requests
import json
from marshmallow import Schema, fields


host = 'd.10jqka.com.cn'
referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/50.0.2661.102 ' \
             'Safari/537.36'

index_hq_url = 'http://d.10jqka.com.cn/v2/realhead/zs_{code}/last.js'
stock_url = 'http://d.10jqka.com.cn/v2/realhead/sz_300342/last.js'

market_id = {
    'sh': 16,
    'sz': 32
}

index_code_map = {
    '000001': '1A0001',
    '000300': '1B0300'
}


class IndexHq(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    price = fields.Decimal(places=2)
    volume = fields.Integer()
    volume_money = fields.Decimal(places=2)
    pre_close = fields.Decimal(places=2)
    open = fields.Decimal(places=2)
    low = fields.Decimal(places=2)
    high = fields.Decimal(places=2)
    bid = fields.Decimal(places=2)
    ask = fields.Decimal(places=2)
    date = fields.Date(format='%Y-%m-%d')
    time = fields.Time(format='%H:%M:%S')


def index_hq_last(code):
    url = index_hq_url.format(code=code)
    headers = {
        'Host': host,
        'Referer': referer,
        'User-Agent': user_agent
    }

    resp = requests.get(stock_url, headers=headers)
    content = resp.content
    text = content[content.find('(')+1:content.rfind(')')]
    jobj = json.loads(text)
    for k, v in jobj['items'].iteritems():
        print k, v
    return jobj


if __name__ == '__main__':
    result = index_hq_last('1A0001')

