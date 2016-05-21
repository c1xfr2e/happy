# coding: utf-8

from datetime import date, datetime, time, timedelta
import pickle
import logging
import tushare as ts
from models import Session, HQ, HSIndex
from indicator.basic import change_percent


def pull_history_hq_of_index(index):
    hqs = ts.get_h_data(index.code, start=str(index.listing_date), index=True, autype='', pause=0.01)
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
            name=index.short_name,
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

        logging.info('[%s][%s]' %(str(index.code), str(from_date)))

    sess.commit()
    logging.info(str(index.code) + ' db session commited')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    index_to_pull = {'000001', '000300', '000003'}
    s = Session()
    for index in s.query(HSIndex).filter(HSIndex.code.in_(index_to_pull)).all():
        pull_history_hq_of_index(index)
