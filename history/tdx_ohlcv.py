# coding: utf-8

from datetime import datetime

f_ohlcv = open('../data/history_ohlcv/600036.txt', 'rb')

while True:
    line = f_ohlcv.readline().decode('gbk').rstrip('\r\n')
    if not line:
        break
    datas = line.split(';')
    date = datetime.strptime(datas[0], '%Y%m%d').date()

    if len(datas) != 7:
        break
    print datas
