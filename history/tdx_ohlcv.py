# coding: utf-8

from datetime import datetime
from decimal import Decimal
from models.history_quote import table_of_quote
from models import Session, engine, Stock


def read_history_quotes(code):
    f_ohlcv = open('../data/history_ohlcv/%s.txt' % code, 'rb')
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
