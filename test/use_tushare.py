# coding: utf8

import tushare as ts

code = '000001'
'''
df_quotes = ts.get_hist_data(code, start='2000-01-01', ktype='D')
indices = df_quotes.index
for i in indices:
    print i
'''

totol_all = ts.get_today_all()

for i in totol_all.index:
    row = totol_all.loc[i]
    print row

fuquan_quotes = ts.get_h_data(code, start='2016-04-15', index=True)
print fuquan_quotes
for i in fuquan_quotes.index:
    row = fuquan_quotes.loc[i]
    print row.open, row.close

current = fuquan_quotes.loc['2016-05-11']
print current
