# coding: utf-8

import re
import requests
from bs4 import BeautifulSoup

url = 'http://stockpage.10jqka.com.cn/{code}/bonus/'


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

    exdiv_shares_and_bonus = u'(\d+)转(\d+)股派(\d*\.\d+|\d+)元'
    exdiv_only_bonus = u'(\d+)派(\d*\.\d+|\d+)元'
    exdiv_only_shares = u'(\d+)转(\d+)股'

    for r in records:
        exdiv_plan = r[u'分红方案说明']


if __name__ == '__main__':
    fetch_exdiv_history('300342')
