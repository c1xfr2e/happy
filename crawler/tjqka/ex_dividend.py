# coding: utf-8

import re
import requests
from decimal import Decimal
from bs4 import BeautifulSoup
from marshmallow import Schema, fields, post_load

url = 'http://stockpage.10jqka.com.cn/{code}/bonus/'


class Dividend(Schema):
    plan = fields.String(load_from=u'分红方案说明')
    ex_date = fields.String(load_from=u'A股除权除息日')
    div_date = fields.String(load_from=u'A股派息日')
    progress = fields.String(load_from=u'方案进度')
    base = fields.Integer()
    cash = fields.Decimal()
    shares = fields.Integer()

    @post_load
    def parse_plan(self, data):
        assert 'plan' in data
        if data['plan'] == u'不分配不转增':
            return None

        plan_shares_and_bonus = u'(\d+)转(\d+)股派(\d*\.\d+|\d+)元'
        plan_only_bonus = u'(\d+)派(\d*\.\d+|\d+)元'
        plan_only_shares = u'(\d+)转(\d+)股'

        m = re.match(plan_shares_and_bonus, data['plan']) or \
            re.match(plan_only_bonus, data['plan']) or \
            re.match(plan_only_shares, data['plan'])
        if not m:
            return None

        groups = m.groups()
        if m.re.pattern == plan_shares_and_bonus:
            data['base'] = int(groups[0])
            data['shares'] = int(groups[1])
            data['cash'] = Decimal(groups[2])
        elif m.re.pattern == plan_only_bonus:
            data['base'] = int(groups[0])
            data['cash'] = Decimal(groups[1])
        elif m.re.pattern == plan_only_shares:
            data['base'] = int(groups[0])
            data['shares'] = int(groups[1])

        return data


class History(Schema):
    dividends = fields.Nested(Dividend, many=True)


def fetch_exdiv_history(code):
    r = requests.get(url.format(code=code))
    soup = BeautifulSoup(r.content)
    bonus_table = soup.find(id='bonus_table')
    head_th_list = bonus_table.find('thead').find_all('th')
    heads = [th.text for th in head_th_list]
    body_tr_list = bonus_table.find('tbody').find_all('tr')

    records = [
        dict(zip(heads, [td.text for td in tr.find_all('td')])) for tr in body_tr_list
    ]

    schema = History()
    result = schema.load({'dividends': records})
    return result.data


if __name__ == '__main__':
    fetch_exdiv_history('300342')
