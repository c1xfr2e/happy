# coding: utf8

import requests
import json
from decimal import Decimal
from collections import OrderedDict
from marshmallow import Schema, fields
from const import market_of_index, tjqka_market_id


time_hq_url = 'http://d.10jqka.com.cn/v2/time/{market_id}_{code}/last.js'

host = 'd.10jqka.com.cn'
referer = 'http://stockpage.10jqka.com.cn/realHead_v2.html'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/50.0.2661.102 ' \
             'Safari/537.36'


class HQTime(Schema):
    name = fields.String()
    date = fields.Date(format='%Y%m%d')
    open = fields.Integer()
    stop = fields.Integer()
    pre_close = fields.Decimal(load_from='pre', places=2)
    hq = fields.Method(load_from='data', deserialize='parse_hq_time')

    def parse_hq_time(self, value):
        time_hq_text = value.split(';')
        hqs = OrderedDict()
        for text in time_hq_text:
            datas = text.split(',')
            hqs[datas[0]] = {
                'price': Decimal(datas[1]),
                'volume_money': Decimal(datas[2]),
                'average': Decimal(datas[3]),
                'volume': Decimal(datas[4])
            }
        return hqs


def hq_time(code, index=False):
    if index:
        market = market_of_index[code]
    else:
        market = 'sh' if code.startswith('6') else 'sz'
    url = time_hq_url.format(market_id=tjqka_market_id[market], code=code)

    headers = {
        'Host': host,
        'Referer': referer,
        'User-Agent': user_agent
    }
    resp = requests.get(url, headers=headers)

    content = resp.content

    text = content[content.find('(') + 1:content.rfind(')')]
    obj = json.loads(text)
    data_key = '%s_%s' % (tjqka_market_id[market], code)
    data_obj = obj[data_key]

    schema = HQTime()
    result = schema.load(data_obj)
    return result.data


if __name__ == '__main__':
    hq_time = hq_time('1A0001', index=True)
    volume = Decimal(0)
    volume_money = Decimal(0)
    for k, v in hq_time['hq'].iteritems():
        print k, v
        volume += v['volume']
        volume_money += v['volume_money']
    print volume, volume_money
