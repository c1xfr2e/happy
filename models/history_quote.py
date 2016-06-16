# coding: utf-8

from sqlalchemy import Table, Column, MetaData
from sqlalchemy import String, DateTime, Numeric, BigInteger

metadata = MetaData()

QuoteBefore2016 = Table(
    'quote_before_2016', metadata,
    Column('code', String(10), primary_key=True),
    Column('datetime', DateTime, primary_key=True),
    Column('period', String(16), primary_key=True),
    Column('open', Numeric(precision=10, scale=3), nullable=False),
    Column('high', Numeric(precision=10, scale=3), nullable=False),
    Column('low', Numeric(precision=10, scale=3), nullable=False),
    Column('close', Numeric(precision=10, scale=3), nullable=False),
    Column('volume', BigInteger, nullable=False),
    Column('amount', BigInteger, nullable=False),
    Column('pre_close', Numeric(precision=10, scale=3), nullable=False),
    Column('change', Numeric(precision=10, scale=3)),
    Column('percent', Numeric(precision=10, scale=3)),
    Column('turnover', Numeric(precision=8, scale=2))
)
