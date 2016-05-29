# coding: utf-8

from datetime import date, time
import logging
import tushare as ts
from models import Session, Quote, Stock
from indicator.basic import change_percent


def pull_history_quotes(security, is_index, start_date=None):
    if not start_date:
        start_date = security.listing_date
    quotes_df = ts.get_h_data(security.code, start=str(start_date), index=is_index, pause=0.01)
    index_riter = reversed(quotes_df.index)
    first = next(index_riter)
    first_hq = quotes_df.loc[first]
    pre_close = first_hq['open']
    sess = Session()

    for timestamp in reversed(quotes_df.index):
        dt = timestamp.to_datetime()
        to_date = from_date = date(dt.year, dt.month, dt.day)
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
            market=security.market,
            code=security.code,
            from_date=from_date,
            to_date=to_date,
            from_time=time(hour=9, minute=15),
            to_time=time(hour=15),
            period='day_1',
            name=security.name,
            open=open,
            close=close,
            low=low,
            high=high,
            pre_close=pre_close,
            change=change,
            change_percent=change_pct,
            volume=volume,
            amount=amount
        )

        sess.merge(quote)
        pre_close = close

        # logging.info('[%s][%s]' %(str(security.code), str(from_date)))

    sess.commit()
    logging.info(str(security.code) + ' db session commited')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    s = Session()
    for stock in s.query(Stock).filter(Stock.status=='L').all():
        pull_history_quotes(stock, is_index=False)
