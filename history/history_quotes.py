# coding: utf-8

import logging
from datetime import date
from decimal import Decimal

from history.tldata.quotes import get_history_quotes
from indicator.basic import change_percent
from models import Stock, Session
from models.history_quote import model_of_quote


def get_and_save_history_quotes(start_date, end_date, code, model):
    quotes = get_history_quotes(start_date, end_date, code)
    m_quotes = []

    for q in quotes:
        adj_factor = q['accumAdjFactor']
        open = Decimal(q['openPrice'] / adj_factor).quantize(Decimal('.001'))
        close = Decimal(q['closePrice'] / adj_factor).quantize(Decimal('.001'))
        low = Decimal(q['lowestPrice'] / adj_factor).quantize(Decimal('.001'))
        high = Decimal(q['highestPrice'] / adj_factor).quantize(Decimal('.001'))
        pre_close = Decimal(q['actPreClosePrice']).quantize(Decimal('.001'))

        m_quote = model(
            code=code,
            datetime=q['tradeDate'],
            period='d',
            open=open,
            close=close,
            low=low,
            high=high,
            pre_close=pre_close,
            change=close - pre_close,
            percent=change_percent(close, pre_close),
            volume=q['turnoverVol'],
            amount=q['turnoverValue'],
            turnover=q['turnoverRate'] * 100
        )

        m_quotes.append(m_quote)

    return m_quotes


if __name__ == '__main__':
    ss = Session()
    stocks = ss.query(Stock.code, Stock.listing_date).all()
    for code, listing_date in stocks:
        quotes = get_and_save_history_quotes(
            listing_date, date(2016, 5, 31), code, model_of_quote(code, listing_date)
        )
        ss.add_all(quotes)
        ss.commit()
