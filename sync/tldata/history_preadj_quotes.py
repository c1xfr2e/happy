# coding: utf-8

import logging
import requests
from datetime import date, time
from decimal import Decimal

from sqlalchemy import and_

from indicator.basic import change_percent
from models import Quote, Stock, Session
from sync.tldata.config import headers

equd_adj_quote_history = 'https://api.wmcloud.com/data/v1/api/market/getMktEqudAdj.json'


def pull_quotes(start, end, codes=None):
    sess = Session()
    criterion = Stock.status == 'L'
    if isinstance(codes, list):
        criterion = and_(criterion, Stock.code.in_(codes))
    stocks = sess.query(Stock).filter(criterion).all()

    for stock in stocks:
        try:
            begin_date = start if start else stock.listing_date
            end_date = end if end else date.today()
            payload = {
                'field': '',
                'beginDate': begin_date.strftime('%Y%m%d'),
                'endDate': end_date.strftime('%Y%m%d'),
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
            quote_records = []
            for data in quotes_data:
                if not data['isOpen']:
                    continue

                adj_factor = data['accumAdjFactor']
                open = Decimal(data['openPrice'] / adj_factor).quantize(Decimal('.001'))
                close = Decimal(data['closePrice'] / adj_factor).quantize(Decimal('.001'))
                low = Decimal(data['lowestPrice'] / adj_factor).quantize(Decimal('.001'))
                high = Decimal(data['highestPrice'] / adj_factor).quantize(Decimal('.001'))
                pre_close = Decimal(data['actPreClosePrice']).quantize(Decimal('.001'))

                quote = Quote(
                    market=stock.market,
                    code=stock.code,
                    from_date=data['tradeDate'],
                    to_date=data['tradeDate'],
                    from_time=time(hour=9, minute=15),
                    to_time=time(hour=15),
                    period='d1',
                    name=stock.name,
                    open=open,
                    close=close,
                    low=low,
                    high=high,
                    pre_close=pre_close,
                    change=close - pre_close,
                    change_percent=change_percent(close, pre_close),
                    volume=data['turnoverVol'],
                    amount=data['turnoverValue'],
                    turnover=data['turnoverRate'] * 100
                )

                quote_records.append(quote)

            sess.add_all(quote_records)
            sess.commit()

        except Exception as e:
            logging.error('Exception: [%s]' % stock.code)
            logging.error(e)
            continue


if __name__ == '__main__':
    start_date = date(2010, 1, 4)
    end_date = date(2010, 1, 8)
    pull_quotes(start_date, end_date, codes=['000418'])
