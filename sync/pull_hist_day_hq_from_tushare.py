# coding: utf-8

from datetime import datetime
import pickle
import tushare as ts
from crawler.const import index_market
from models.hq import HQ
from models import Session
from indicator.basic import change_percent


def pull_index_day_hq_from_2000(code):
    market = index_market[code]
    # hqs = ts.get_h_data(code, start='2010-06-01', index=True, autype='')
    # pickle.dump(hqs, open('../data/399006.hq', 'wb'))

    hqs = pickle.load(open('../data/399006.hq', 'rb'))
    iterator = reversed(hqs.index)
    first_index = next(iterator)
    first_day_hq = hqs.loc[first_index]
    pre_close = first_day_hq['open']
    for i in reversed(hqs.index):
        row = hqs.loc[i]
        print row['open'], row['close']


    pre_close = 0
    change = 0
    change_pct = 0
    start_datetime = ''
    end_datetime = ''

    hq = {}

    hq_day = HQ(
        market=market,
        code=code,
        from_dt=start_datetime,
        to_dt=end_datetime,
        period='day',
        name='',
        open=hq['open'],
        close=hq['close'],
        low=hq['low'],
        hight=hq['high'],
        pre_close=pre_close,
        change=change,
        change_percent=change_percent,
        volume=hq['volume'],
        amount=hq['amount'],
        turnover=0
    )

    sess = Session()
    sess.add(hq_day)

    sess.commit()


if __name__ == '__main__':
    pull_index_day_hq_from_2000('399006')
