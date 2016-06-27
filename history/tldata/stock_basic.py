# coding: utf-8

import logging

import requests

from history.tldata.config import headers
from models import Stock, Session

url_stock_basic = 'https://api.wmcloud.com/data/v1/api/equity/getEqu.json'
url_cnspell = 'https://api.wmcloud.com/data/v1/api/master/getSecID.json'


def get_stock_basic(code):
    payload = {
        'field': '',
        'ticker': code,
        'secID': '',
        'equTypeCD': '',
        'listStatusCD': ''
    }
    resp = requests.get(url_stock_basic, headers=headers, params=payload)
    json_res = resp.json()
    if json_res['retCode'] != 1:
        logging.error('Request failed: [%s] %s' % (code, json_res['retMsg']))
        return None
    return json_res['data'][0]


def get_cnspell(ticker):
    payload = {
        'field': 'cnSpell',
        'ticker': ticker
    }
    try:
        resp = requests.get(url_cnspell, headers=headers, params=payload)
        json_res = resp.json()
        if json_res['retCode'] != 1:
            logging.error('Request failed: [%s] %s' % (ticker, json_res['retMsg']))
            return None
        return json_res['data'][0]['cnSpell']
    except Exception as e:
        logging.error(e)
        return None

if __name__ == '__main__':
    sess = Session()
    stocks = sess.query(Stock).filter(Stock.pinyin.is_(None)).all()

    for stock in stocks:
        stock_data = get_stock_basic(stock.code)
        for data in stock_data:
            sess.query(Stock).filter(Stock.code == stock.code).update(
                {
                    'full_name': data['secFullName'],
                    'pinyin': get_cnspell(stock.code),
                    'status': data['listStatusCD']
                }
            )

    sess.commit()
