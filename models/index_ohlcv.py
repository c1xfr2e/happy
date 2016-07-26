# coding: utf-8

from sqlalchemy import Column, String, DateTime, Numeric, BigInteger, Index, UniqueConstraint
from . import Base


class IndexOhlcv(Base):
    __tablename__ = 'index_ohlcv'

    code = Column(String(10), primary_key=True)
    datetime = Column(DateTime, primary_key=True)
    period = Column(String(16), primary_key=True)

    open = Column(Numeric(precision=10, scale=3), nullable=False)
    high = Column(Numeric(precision=10, scale=3), nullable=False)
    low = Column(Numeric(precision=10, scale=3), nullable=False)
    close = Column(Numeric(precision=10, scale=3), nullable=False)
    volume = Column(BigInteger, nullable=False)
    amount = Column(BigInteger, nullable=False)

    __table_args__ = (
        Index('code_period', 'code', 'period'),
        Index('datetime_period', 'datetime', 'period')
    )
