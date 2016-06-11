# coding: utf-8

from datetime import date, time
import logging
import tushare as ts
from models import Session, HSIndex, Quote
from indicator.basic import change_percent


def pull_history_hq_of_index(index, start_date=None, end_date=None):
    if not start_date:
        start_date = index.listing_date
    hqs = ts.get_h_data(index.code, start=str(start_date), end=str(end_date),
                        index=True, autype='', pause=0.01)
    iterator = reversed(hqs.index)
    first_index = next(iterator)
    first_day_hq = hqs.loc[first_index]
    pre_close = first_day_hq['open']
    sess = Session()

    for timestamp in reversed(hqs.index):
        dt = timestamp.to_datetime()
        datetime_ = date(dt.year, dt.month, dt.day)
        row = hqs.loc[timestamp]

        open_price = row['open']
        close = row['close']
        low = row['low']
        high = row['high']
        volume = row['volume']
        amount = row['amount']
        change = close - pre_close
        change_pct = change_percent(close, pre_close)

        hq_day = Quote(
            market=index.market,
            code=index.code,
            datetime=datetime_,
            period='d1',
            name=index.name,
            open=open_price,
            close=close,
            low=low,
            high=high,
            pre_close=pre_close,
            change=change,
            percent=change_pct,
            volume=volume,
            amount=amount
        )

        sess.merge(hq_day)

        pre_close = close

        logging.info('[%s][%s]' %(str(index.code), str(datetime_)))

    sess.commit()
    logging.info(str(index.code) + ' db session commited')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    index_to_pull = {
        '000001',
        '000016',
        '000300',
        '000905',
        '399001',
        '399006',
        '399102'
    }
    start = date(2016, 5, 30)
    end = date(2016, 6, 1)
    s = Session()
    for index in s.query(HSIndex).filter(HSIndex.code.in_(index_to_pull)).all():
        pull_history_hq_of_index(index, start, end)
