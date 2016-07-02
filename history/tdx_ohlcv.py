# coding: utf-8

from datetime import datetime
from decimal import Decimal
from models.history_quote import model_of_quote

f_ohlcv = open('../data/history_ohlcv/600036.txt', 'rb')

while True:
    line = f_ohlcv.readline().decode('gbk').rstrip('\r\n')
    if not line:
        break
    data = line.split(';')
    if len(data) != 7:
        break

    date = datetime.strptime(data[0], '%Y%m%d').date()
    open = Decimal(data[1])
    high = Decimal(data[2])
    low = Decimal(data[3])
    close = Decimal(data[4])
    volume = int(data[5])
    amount = int(data[6])

