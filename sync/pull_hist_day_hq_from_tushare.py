# coding: utf-8

from datetime import date, datetime, time, timedelta
import pickle
import tushare as ts
from crawler.const import index_market
from models import Session, HQ, HSIndex
from indicator.basic import change_percent


def pull_history_hq_of_index(index):
    hqs = ts.get_h_data(index.code, start=index.listing_date, index=True, autype='')
    # pickle.dump(hqs, open('../data/399006.hq', 'wb'))
    #hqs = pickle.load(open('../data/399006.hq', 'rb'))
    iterator = reversed(hqs.index)
    first_index = next(iterator)
    first_day_hq = hqs.loc[first_index]
    pre_close = first_day_hq['open']
    sess = Session()

    for timestamp in reversed(hqs.index):
        dt = timestamp.to_datetime()
        to_date = from_date = date(dt.year, dt.month, dt.day)
        row = hqs.loc[timestamp]

        open_price = row['open']
        close = row['close']
        low = row['low']
        high = row['high']
        volume = row['volume']
        amount = row['amount']
        change = close - pre_close
        change_pct = change_percent(close, pre_close)

        hq_day = HQ(
            market=index.market,
            code=index.code,
            from_date=from_date,
            to_date=to_date,
            from_time=time(hour=9, minute=15),
            to_time=time(hour=15),
            period='day_1',
            name=index.name,
            open=open_price,
            close=close,
            low=low,
            high=high,
            pre_close=pre_close,
            change=change,
            change_percent=change_pct,
            volume=volume,
            amount=amount
        )

        sess.add(hq_day)

        pre_close = close

    sess.commit()


if __name__ == '__main__':
    s = Session()
    cyb_index = s.query(HSIndex).filter(HSIndex.code=='399006').first()
    print cyb_index
    pull_history_hq_of_index(cyb_index)
