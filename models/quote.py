# coding: utf-8

from sqlalchemy import Column, String, DateTime, Time, Numeric, BigInteger
from . import Base


class Quote(Base):
    __tablename__ = 'quote'

    market = Column(String(16), primary_key=True)
    code = Column(String(10), primary_key=True)
    datetime = Column(DateTime, primary_key=True)
    period = Column(String(16), primary_key=True)

    name = Column(String(16))

    open = Column(Numeric(precision=10, scale=3), nullable=False)
    high = Column(Numeric(precision=10, scale=3), nullable=False)
    low = Column(Numeric(precision=10, scale=3), nullable=False)
    close = Column(Numeric(precision=10, scale=3), nullable=False)
    volume = Column(BigInteger, nullable=False)
    amount = Column(BigInteger, nullable=False)

    pre_close = Column(Numeric(precision=10, scale=3), nullable=False)
    change = Column(Numeric(precision=10, scale=3))
    percent = Column(Numeric(precision=8, scale=3))

    turnover = Column(Numeric(precision=8, scale=2))
