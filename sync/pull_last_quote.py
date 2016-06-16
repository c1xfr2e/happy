# coding: utf8

from datetime import date
from crawler.tjqka.hq_last import hq_last
from models import Quote, Session, Stock
from indicator.basic import change_percent


def pull_last_quote(security, is_index):
    hq = hq_last(security.market, security.code, is_index)

    open = hq.get('open', 0)
    # SUSPEND TODAY
    if open == 0:
        high, low, close, pre_close, volume, amount, change, percent = 0, 0, 0, 0, 0, 0, 0, 0
        return None
    else:
        close = hq.get('close', 0)
        low = hq.get('low', 0)
        high = hq.get('high', 0)
        pre_close = hq.get('pre_close', 0)
        volume = hq.get('volume', 0)
        amount = hq.get('amount', 0)
        change = hq.get('change', 0) or hq.get('close', 0) - hq.get('pre_close', 0)
        percent = hq.get('change_percent') or change_percent(close, pre_close) if pre_close else 0

    quote = Quote(
        code=security.code,
        datetime=date.today(),
        period='d1',
        open=open,
        close=close,
        low=low,
        high=high,
        pre_close=pre_close,
        change=change,
        percent=percent,
        volume=volume,
        amount=amount
    )

    if is_index:
        if security.alias:
            quote.code = security.alias
    else:
        turnover = volume / security.tradable_shares * 100 if security.tradable_shares > 0 else 0
        quote.turnover = round(turnover, 2)

    return quote


if __name__ == '__main__':
    sess = Session()

    stocks = sess.query(Stock).filter(Stock.status == 'L').all()
    # stocks = sess.query(Stock).filter(Stock.code == '600035').all()
    for stock in stocks:
        pull_last_quote(stock, False)

    '''
    index_code_to_sync = [
        '000001',
        '000003',
        '000016'
        '000300',
        '399001',
        '399006',
        '399102'
    ]

    for index in sess.query(HSIndex).filter(HSIndex.code.in_(index_code_to_sync)).all():
        pull_last_quote(index, True)
    '''
