# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = 'rdsbi4u1v33wc6zn0w71o.mysql.rds.aliyuncs.com'
user = 'zh'
passwd = '000000'
database = 'alchemist'
param_charset = 'charset=utf8'
url = 'mysql://{user}:{passwd}@{host}/{database}?{params}'

aliyun_mysql_url = url.format(
    host=host, user=user, passwd=passwd, database=database, params=param_charset
)
engine = create_engine(aliyun_mysql_url, encoding='utf-8')
Base = declarative_base()

# Base.metadata.bind = engine
# Session = sessionmaker(bind=engine)

from security_exchange import SecurityExchange
from stock_profile import StockProfile
from hq import HQ
from hq_snapshot import HQSnapshot
from hs_index import HSIndex

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

'''
snapshot = HQSnapshot(
    code='399006',
    name=u'创业板指',
    date='20160517',
    time='15:00',
    price=2022.38,
    pre_close=2031.21,
    open=2000.1,
    low=1998,
    high=2088.03,
    volume=1000000,
    volume_money=123456789
)

session = Session()
session.add(snapshot)
session.commit()

hq_snapshots = session.query(HQSnapshot).filter(HQSnapshot.code=='399006').all()
for hq in hq_snapshots:
    print hq.name, hq.price
'''
