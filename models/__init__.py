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
from hs_index import HSIndex
from stock import Stock
from quote import Quote
from index_ohlcv import IndexOhlcv

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
