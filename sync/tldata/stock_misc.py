# coding: utf-8

import requests
import logging
from models import Stock, Session
from sync.tldata.config import headers


url_stock_info = 'https://api.wmcloud.com/data/v1/api/equity/getEqu.json'
url_cnspell = 'https://api.wmcloud.com/data/v1/api/master/getSecID.json'


def pull_cnspell(ticker):
    payload = {
        'field': 'cnSpell',
        'ticker': ticker
    }
    try:
        resp = requests.get(url_cnspell, headers=headers, params=payload)
        json_res = resp.json()
        if json_res['retCode'] != 1:
            logging.error('Request failed: [%s] %s' % (stock.code, json_res['retMsg']))
            return None
        return json_res['data'][0]['cnSpell']
    except Exception as e:
        logging.error(e)
        return None


sess = Session()
stocks = sess.query(Stock).all()

for stock in stocks:
    payload = {
        'field': '',
        'ticker': stock.code,
        'secID': '',
        'equTypeCD': '',
        'listStatusCD': ''
    }
    resp = requests.get(url_stock_info, headers=headers, params=payload)
    json_res = resp.json()
    if json_res['retCode'] != 1:
        logging.error('Request failed: [%s] %s' % (stock.code, json_res['retMsg']))
        continue

    stock_data = json_res['data']
    for data in stock_data:
        sess.query(Stock).filter(Stock.code == stock.code).update(
            {
                'full_name': data['secFullName'],
                'pinyin': pull_cnspell(stock.code),
                'status': data['listStatusCD']
            }
        )

sess.commit()

'''
listSectorCD 1
exchangeCD XSHG
secID 600000.XSHG
secFullName 上海浦东发展银行股份有限公司
secShortNameEn Pudong Dev
listDate 1999-11-10 00:00:00
secShortName 浦发银行
secFullNameEn Shanghai Pudong Development Bank Co.,Ltd.
listStatusCD L
partyID 603
cnSpell PFYH
ticker 600000
equTypeCD 0201010201
'''
