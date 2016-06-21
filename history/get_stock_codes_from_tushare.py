# coding: utf-8

from db.mongo import client
import tushare as ts

stock_basics = ts.get_stock_basics()  # This is a Pandas DateFrame object which stock_code is used as index.
codes = [{'code': code} for code in stock_basics.index]

c_stock_codes = client.alchemist.stock_codes
c_stock_codes.insert(codes)
