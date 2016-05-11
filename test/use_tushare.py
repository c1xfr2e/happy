# coding: utf8

import tushare as ts

code = '000001'
'''
df_quotes = ts.get_hist_data(code, start='2000-01-01', ktype='D')
indices = df_quotes.index
for i in indices:
    print i
'''

fuquan_quotes = ts.get_h_data(code, start='2016-04-15', index=True)
print fuquan_quotes
for i in fuquan_quotes.index:
    row = fuquan_quotes.loc[i]
    print row, type(row)

current = fuquan_quotes.loc['2016-05-11']
print current
