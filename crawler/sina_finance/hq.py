# coding: utf-8

import requests
import re
import time
from collections import OrderedDict

url_format = 'http://hq.sinajs.cn/list={market}{code}'


def hq_lastest(market, code):
    keys = [
        'name',
        'open_price',
        'pre_close_price',
        'latest_price',
        'high_price',
        'low_price',
        'bid_price',
        'ask_price',
        'volume_shares',
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
    datas = data_text.split(',')
    kv = OrderedDict(zip(keys, datas))
    for k, v in kv.iteritems():
        print k, v


if __name__ == '__main__':
    hq_lastest('sz', '399006')
