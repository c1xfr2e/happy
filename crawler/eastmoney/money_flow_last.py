# coding: utf-8

"""
    Realtime money flow.
"""

import requests
import re
import random
from marshmallow import Schema, fields


index_url = 'http://s1.dfcfw.com/js/zs{code}.js?rt={random}'
stock_url = 'http://s1.dfcfw.com/js/{code}.js?rt={random}'

"""
    data = [
        -1983.40,   # 0  主力净流入(万）
        -8.03,      # 1  主力净比 (%)
        -446.06,    # 2  超大单净流入
        -1.81,      # 3  超大单净比
        -1537.34,   # 4  大单净流入
        -6.22,      # 5  大单净比
        668.12,     # 6  中单净流入
        2.70,       # 7  中单净比
        1315.28,    # 8  小单净流入
        5.32,       # 9  小单净比
        0.00,       # 10 ?
        0.00,       # 11 ?
        1332.64,    # 12 超大单流入
        -1778.71,   # 13 超大单流出
        7209.15,    # 14 大单流入
        -8746.49,   # 15 大单流出
        8989.29,    # 16 中单流入
        -8321.17,   # 17 中单流出
        7144.82,    # 18 小单流入
        -5829.54,   # 19 小单流出
        23343.26,   # 20 ?
        -22897.20   # 21 ?
    ]
"""


class MoneyFlow(Schema):
    class Meta:
        ordered = True
    main_force_net = fields.Decimal(load_from=0, places=2)
    main_force_ratio = fields.Decimal(load_from=1, places=2)
    super_big_net = fields.Decimal(load_from=2, places=2)
    super_big_ratio = fields.Decimal(load_from=3, places=2)
    big_net = fields.Decimal(load_from=4, places=2)
    big_ratio = fields.Decimal(load_from=5, places=2)
    medium_net = fields.Decimal(load_from=6, places=2)
    medium_ratio = fields.Decimal(load_from=7, places=2)
    small_net = fields.Decimal(load_from=8, places=2)
    small_ratio = fields.Decimal(load_from=9, places=2)
    super_big_in = fields.Decimal(load_from=12, places=2)
    super_big_out = fields.Decimal(load_from=13, places=2)
    big_in = fields.Decimal(load_from=14, places=2)
    big_out = fields.Decimal(load_from=15, places=2)
    medium_in = fields.Decimal(load_from=16, places=2)
    medium_out = fields.Decimal(load_from=17, places=2)
    small_in = fields.Decimal(load_from=18, places=2)
    small_out = fields.Decimal(load_from=19, places=2)


def money_flow_last(code, is_index):
    if is_index:
        url = index_url.format(code=code, random=random.random())
    else:
        url = stock_url.format(code=code, random=random.random())
    resp = requests.get(url)
    groups = re.findall('data:\"(.*)\",update:\"(.*)\"', resp.content)
    if not groups:
        return None

    datas_text = groups[0][0]
    time_text = groups[0][1]

    datas = datas_text.split(',')
    datas.append(time_text)

    data_dict = dict(zip(range(0, len(datas)), datas))

    quote_data = MoneyFlow()
    result = quote_data.load(data_dict)

    return result.data


if __name__ == '__main__':
    result = money_flow_last('000001', True)
    for k, v in result.iteritems():
        print k, v
