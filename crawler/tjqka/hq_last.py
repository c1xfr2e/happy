# coding: utf-8

import requests
import json
from marshmallow import Schema, fields
from crawler.util import stock_market

host = 'd.10jqka.com.cn'
referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/50.0.2661.102 ' \
             'Safari/537.36'

index_hq_url = 'http://d.10jqka.com.cn/v2/realhead/zs_{code}/last.js'
stock_url = 'http://d.10jqka.com.cn/v2/realhead/{market}_{code}/last.js'


class HQSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    price = fields.Decimal(load_from='10', places=2)
    change = fields.Decimal(load_from='264648', places=2)
    change_percent = fields.Decimal(load_from='199112', places=2)
    volume = fields.Decimal(load_from='13', places=0)
    volume_money = fields.Decimal(load_from='19', places=2)
    pre_close = fields.Decimal(load_from='6', places=2)
    open = fields.Decimal(load_from='7', places=2)
    low = fields.Decimal(load_from='9', places=2)
    high = fields.Decimal(load_from='8', places=2)
    bid_ask_ratio = fields.Decimal(load_from='461256', places=2)
    bid_ask_diff = fields.Decimal(load_from='395720', places=0)
    in_size = fields.Decimal(load_from='15', places=0)
    out_size = fields.Decimal(load_from='14', places=0)


def hq_last(code, index=False):
    if index:
        url = index_hq_url.format(code=code)
    else:
        url = stock_url.format(market=stock_market(code), code=code)

    # Fake headers. Necessery?
    headers = {
        'Host': host,
        'Referer': referer,
        'User-Agent': user_agent
    }
    resp = requests.get(url, headers=headers)

    content = resp.content
    text = content[content.find('(')+1:content.rfind(')')]
    obj = json.loads(text)

    schema = HQSchema()
    result = schema.load(obj['items'])
    return result.data


if __name__ == '__main__':
    result = hq_last('300342')
    for k,v in result.iteritems():
        print k, v
    # result = hq_last('1A0001')
