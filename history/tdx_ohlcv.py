# coding: utf-8

import logging
from datetime import datetime
from decimal import Decimal
from models.history_quote import table_of_quote
from models import Session, engine, Stock, IndexOhlcv


def read_tdx_ohlcv(filepath):
    f_ohlcv = open(filepath, 'rb')
    datas = []
    while True:
        line = f_ohlcv.readline().decode('gbk').rstrip('\r\n')
        if not line:
            break
        data = line.split(';')
        if len(data) != 7:
            logging.warning(filepath + line)
            continue

        datas.append((
            datetime.strptime(data[0], '%Y%m%d').date(),  # date
            Decimal(data[1]),  # open
            Decimal(data[2]),  # high
            Decimal(data[3]),  # low
            Decimal(data[4]),  # close
            int(data[5]),      # volume
            float(data[6])     # amount
        ))
    return datas


def read_history_quotes(code):
    f_ohlcv = open('data/history_ohlcv/%s.txt' % code, 'rb')
    inserts = []
    while True:
        line = f_ohlcv.readline().decode('gbk').rstrip('\r\n')
        if not line:
            break
        data = line.split(';')
        if len(data) != 7:
            break

        date_ = datetime.strptime(data[0], '%Y%m%d').date()
        open_ = Decimal(data[1])
        high = Decimal(data[2])
        low = Decimal(data[3])
        close = Decimal(data[4])
        volume = int(data[5])
        amount = float(data[6])

        table = table_of_quote(code, date_)
        ins = table.insert().values(
            code=code,
            datetime=date_,
            period='d',
            open=open_,
            close=close,
            low=low,
            high=high,
            volume=volume,
            amount=amount
        )
        inserts.append(ins)

    return inserts


def import_stock_history_ohlcv():
    ss = Session()
    conn = engine.connect()
    stocks = ss.query(Stock.code).all()
    for stock in stocks:
        quote_inserts = read_history_quotes(stock.code)
        for ins in quote_inserts:
            try:
                conn.execute(ins)
            except Exception as e:
                continue


def import_index_history_ohlcv():
    indices = ['000001', '399001', '399006', '000016']
    for i in indices:
        datas = read_tdx_ohlcv('../data/index_history/%s.txt' % i)
        records = [
            IndexOhlcv(
                code=i,
                datetime=data[0],
                period='d',
                open=data[1],
                high=data[2],
                low=data[3],
                close=data[4],
                volume=data[5],
                amount=data[6]
            )
            for data in datas
        ]

        ss = Session()
        ss.add_all(records)
        ss.commit()


if __name__ == '__main__':
    import_index_history_ohlcv()
