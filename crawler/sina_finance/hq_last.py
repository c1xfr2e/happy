# coding: utf-8

import requests
import re
from collections import OrderedDict
from decimal import Decimal
from marshmallow import Schema, fields

import logging
from config import log_format
logging.basicConfig(format=log_format)

url_format = 'http://hq.sinajs.cn/list={market}{code}'


class HQSchema(Schema):
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


def hq_last(market, code):
    keys = [
        'name',
        'open',
        'pre_close',
        'price',
        'high',
        'low',
        'bid',
        'ask',
        'volume',
        'volume_money',
        'bid_1_count',
        'bid_1_price',
        'bid_2_count',
        'bid_2_price',
        'bid_3_count',
        'bid_3_price',
        'bid_4_count',
        'bid_4_price',
        'bid_5_count',
        'bid_5_price',
        'ask_1_count',
        'ask_1_price',
        'ask_2_count',
        'ask_2_price',
        'ask_3_count',
        'ask_3_price',
        'ask_4_count',
        'ask_4_price',
        'ask_5_count',
        'ask_5_price',
        'date',
        'time',
        '_'
    ]

    url = url_format.format(market=market, code=code)
    resp = requests.get(url)
    content = resp.content.decode('gbk')
    data_text = re.findall('"(.*)"', content)[0]
    data_list = data_text.split(',')
    kvs = OrderedDict(zip(keys, data_list))

    schema = HQSchema()
    result = schema.load(kvs)
    if result.errors:
        msg = '[%s] %s' % (code, result.errors)
        logging.error(msg)

    return result.data


if __name__ == '__main__':
    print hq_last('sh', '000001')
