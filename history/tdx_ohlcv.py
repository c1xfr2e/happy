# coding: utf-8

from datetime import date

f_ohlcv = open('../data/history_ohlcv/600036.txt', 'rb')

line = f_ohlcv.readline().decode('gbk').rstrip('\r\n')
datas = line.split(';')
print datas
