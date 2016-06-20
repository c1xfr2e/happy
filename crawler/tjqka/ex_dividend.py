# coding: utf-8

import re
import requests
from decimal import Decimal
from bs4 import BeautifulSoup
from marshmallow import Schema, fields, pre_load, post_load

url = 'http://stockpage.10jqka.com.cn/{code}/bonus/'


class Dividend(Schema):
    board_date = fields.String(load_from=u'董事会日期')
    holders_date = fields.String(load_from=u'股东大会日期')
    record_date = fields.String(load_from=u'A股股权登记日')
    execution_date = fields.String(load_from=u'实施日期')
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
        else:
            assert False

        return data


class Allotment(Schema):
    plan = fields.String(load_from=u'实际配股比例')
    ex_date = fields.String(load_from=u'除权日')
    base = fields.Integer()
    shares = fields.Decimal()

    @post_load
    def post_parse(self, data):
        plan_items = data['plan'].split(' ')
        data['base'] = int(plan_items[0])
        data['shares'] = Decimal(plan_items[2])
        return data


class History(Schema):
    dividends = fields.Nested(Dividend, many=True)
    allotments = fields.Nested(Allotment, many=True)


def fetch_exdiv_history(code):
    r = requests.get(url.format(code=code))
    soup = BeautifulSoup(r.content)

    # Dividend history table.
    bonus_table = soup.find(id='bonus_table')
    head_th_list = bonus_table.find('thead').find_all('th')
    heads = [th.text for th in head_th_list]
    body_tr_list = bonus_table.find('tbody').find_all('tr')

    div_history = []
    for tr in body_tr_list:
        datas = dict(zip(heads, [td.text for td in tr.find_all('td')]))
        if datas.get(u'分红方案说明') == u'不分配不转增':
            continue
        div_history.append(datas)

    # Allotment history table.
    allot_div = soup.find(id='stockallotdata')
    allot_tables = allot_div.find_all('table', class_='m_table pggk mt10')
    allot_history = []
    for table in allot_tables:
        tds = table.find_all('td')
        plan_k, plan_v = tds[0].text.split(u'：')
        exdate_k, exdate_v = tds[9].text.split(u'：')
        allot_history.append({
            plan_k: plan_v,
            exdate_k: exdate_v
        })

    schema = History()
    result = schema.load({
        'dividends': div_history,
        'allotments': allot_history
    })
    return result.data


if __name__ == '__main__':
    fetch_exdiv_history('600036')
