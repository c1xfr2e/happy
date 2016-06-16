# coding: utf-8

from datetime import date
import logging
from sqlalchemy import and_
import tushare as ts
from models import Session, Quote, Stock
from indicator.basic import change_percent
from db.mongo import client


def pull_history_quotes(security, is_index, start_date=None, end_date=None):
    if not start_date or start_date < security.listing_date:
        start_date = security.listing_date

    try:
        quotes_df = ts.get_h_data(security.code, start=str(start_date), end=str(end_date), index=is_index, pause=0.01)
    except:
        result = client.alchemist.pull_hist_failed.update(
            {'market': security.market, 'code': security.code},
            {'market': security.market, 'code': security.code, 'reason': 'ts.get_h_data throw exception'},
            upsert=True
        )
        logging.error('Pull tushare history quotes failed.')
        logging.error(result)
        return

    index_riter = reversed(quotes_df.index)
    first = next(index_riter)
    first_hq = quotes_df.loc[first]
    pre_close = first_hq['open']
    sess = Session()

    for timestamp in reversed(quotes_df.index):
        dt = timestamp.to_datetime()
        datetime_ = date(dt.year, dt.month, dt.day)

        row = quotes_df.loc[timestamp]

        open = row['open']
        high = row['high']
        low = row['low']
        close = row['close']
        volume = row['volume']
        amount = row['amount']

        change = close - pre_close
        change_pct = change_percent(close, pre_close)

        '''
        turnover = None
        if security.tradable_shares != 0:
            turnover = volume / security.tradable_shares * 100
        '''

        quote = Quote(
            code=security.code,
            datetime=datetime_,
            period='d1',
            open=open,
            close=close,
            low=low,
            high=high,
            pre_close=pre_close,
            change=change,
            percent=change_pct,
            volume=volume,
            amount=amount
        )

        sess.merge(quote)
        pre_close = close

    try:
        sess.commit()
        logging.info(str(security.code) + ' db session commited')
    except:
        result = client.alchemist.pull_hist_failed.update(
            {'market': security.market, 'code': security.code},
            {'market': security.market, 'code': security.code, 'reason': 'session commit exception'},
            upsert=True
        )
        logging.error('Session commit failed.')
        logging.error(result)
        return


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    s = Session()

    done_codes = s.query(Quote.code.distinct()).subquery()
    stocks_to_pull = s.query(Stock).filter(and_(
        Stock.status == 'L',
        Stock.code.notin_(done_codes)
    )).all()

    stocks_to_pull = s.query(Stock).filter(Stock.code=='000418').all()
    start_date = date(2010, 1, 4)
    end_date = date(2010, 1, 13)
    for stock in stocks_to_pull:
        pull_history_quotes(stock, is_index=False, start_date=start_date, end_date=end_date)
