# coding: utf-8

import MySQLdb
db = MySQLdb.connect(
    host='rdsbi4u1v33wc6zn0w71o.mysql.rds.aliyuncs.com',
    user='zh', passwd='000000', db='alchemist'
)
cursor = db.cursor()
cursor.execute('select id from ticker')
results = cursor.fetchall()
for int_ticker in results:
    str_ticker = '{0:0>6}'.format(int_ticker[0])
    cursor.execute('insert into hs_ticker values("%s")' % str_ticker)

db.commit()
db.close()
