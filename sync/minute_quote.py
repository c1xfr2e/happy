# coding: utf-8

from datetime import date

min5_quotes = open('../data/min_quote/SH#000001.txt', 'rb')
min5_quotes.readline()
min5_quotes.readline()

line = min5_quotes.readline().decode('gbk').rstrip('\r\n')
datas = line.split(';')
print datas
