# coding: utf8

import tushare as ts

code = '300059'

# 股票历史行情
all_quotes = ts.get_hist_data(code, start='2016-04-15', ktype='D')
print all_quotes
# 前复权日线数据
fuquan_quotes = ts.get_h_data(code, start='2016-04-15')
print all_quotes
