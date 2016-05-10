# coding: utf8

import tushare as ts

code = '600597'
all_quotes = ts.get_hist_data('600848')
print all_quotes

