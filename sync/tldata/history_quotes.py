# coding: utf-8

import logging
import requests
from datetime import date, time

from indicator.basic import change_percent
from models import Quote, Stock, Session
from sync.tldata.config import headers


equd_adj_quote_history = 'https://api.wmcloud.com/data/v1/api/market/getMktEqudAdj.json'

sess = Session()
stocks = sess.query(Stock).filter(Stock.status == 'L').all()
for stock in stocks:
    try:
        payload = {
            'field': '',
            'beginDate': stock.listing_date.strftime('%Y%m%d'),
            'endDate': date.today().strftime('%Y%m%d'),
            'secID': '',
            'ticker': stock.code,
            'tradeDate': ''
        }

        resp = requests.get(equd_adj_quote_history, headers=headers, params=payload)
        json_res = resp.json()
        if json_res['retCode'] != 1:
            logging.error('Request failed: [%s] %s' % (stock.code, json_res['retMsg']))
            continue

        quotes_data = json_res['data']
        for data in quotes_data:
            quote = Quote(
                market=stock.market,
                code=stock.code,
                from_date=data['tradeDate'],
                to_date=data['tradeDate'],
                from_time=time(hour=9, minute=15),
                to_time=time(hour=15),
                period='day_1',
                name=stock.name,
                open=data['openPrice'],
                close=data['closePrice'],
                low=data['lowestPrice'],
                high=data['highestPrice'],
                pre_close=data['preClosePrice'],
                change=data['closePrice'] - data['preClosePrice'],
                change_percent=change_percent(data['closePrice'], data['preClosePrice']),
                volume=data['turnoverVol'],
                amount=data['turnoverValue'],
                turnover=data['turnoverRate'] * 100
            )
            sess.merge(quote)
        sess.commit()

    except Exception as e:
        logging.error('Exception: [%s]' % stock.code)
        logging.error(e)
        continue
