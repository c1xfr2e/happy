# coding: utf-8

from datetime import datetime
import tushare as ts
from models import Session, Stock
from history.tldata.stock_basic import get_stock_basic, get_cnspell


if __name__ == '__main__':
    ss = Session()
    current_codes = [_[0] for _ in ss.query(Stock.code).all()]

    stocks_from_ts = ts.get_stock_basics()  # This is a Pandas DateFrame object which stock_code is used as index.
    codes_from_ts = [code for code in stocks_from_ts.index]

    new_codes = set(codes_from_ts) - set(current_codes)
    for code in new_codes:
        basic = get_stock_basic(code)
        if basic:
            stock = Stock(
                market='sh' if code[0] == '6' else 'sz',
                code=code,
                name=basic[u'secShortName'],
                status=basic['listStatusCD'],
                pinyin=get_cnspell(code),
                update_time=datetime.now()
            )
            ss.add(stock)
    ss.commit()
