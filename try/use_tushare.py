# coding: utf8

import tushare as ts
from tushare.util import dateu

cal = dateu.trade_cal()

code = '000001'

df_quotes = ts.get_hist_data('sh', start='2010-01-01', ktype='D')
print df_quotes
indices = df_quotes.index

'''
totol_all = ts.get_realtime_quotes('300342')
for i in totol_all.index:
    row = totol_all.loc[i]
    print row
'''


fuquan_quotes = ts.get_h_data('000001', start='2010-01-01', index=True, autype=None)
print fuquan_quotes
# for i in fuquan_quotes.index:
#    row = fuquan_quotes.loc[i]
#    print row

# current = fuquan_quotes.loc['2016-05-11']
# print current
'''
date        open   high   close    low      volume       amount
2016-05-19  10.05  10.20   9.91   9.88  18438060.0  184991239.0
2016-05-18  10.20  10.27  10.03   9.92  22521753.0  227346981.0
2016-05-17  10.85  10.85  10.43  10.41  26326270.0  278596368.0
2016-05-16  14.15  14.38  14.32  13.74  24439280.0  343605438.0
2016-05-13  14.09  14.46  14.28  13.99  24460789.0  347914761.0
2016-05-12  14.00  14.18  14.12  13.68  35142378.0  490320233.0
2016-05-11  13.60  14.86  14.44  13.60  55445760.0  803479362.0
'''
