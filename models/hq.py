# coding: utf-8

from sqlalchemy import Column, String, DateTime, Numeric, BigInteger
from . import Base


class HQ(Base):
    __tablename__ = 'hq'

    market = Column(String(16), primary_key=True)
    code = Column(String(10), primary_key=True)
    from_datetime = Column(DateTime, primary_key=True)
    to_datetime = Column(DateTime, primary_key=True)

    period = Column(String(16), nullable=False)
    name = Column(String(16))

    open = Column(Numeric(precision=10, scale=3), nullable=False)
    close = Column(Numeric(precision=10, scale=3), nullable=False)
    low = Column(Numeric(precision=10, scale=3), nullable=False)
    high = Column(Numeric(precision=10, scale=3), nullable=False)

    pre_close = Column(Numeric(precision=10, scale=3), nullable=False)
    change = Column(Numeric(precision=10, scale=3))
    change_percent = Column(Numeric(precision=8, scale=3))

    volume = Column(BigInteger, nullable=False)
    amount = Column(BigInteger, nullable=False)

    turnover = Column(Numeric(precision=8, scale=2))
