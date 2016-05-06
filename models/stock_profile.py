# coding: utf-8

from sqlalchemy import Column, Integer, Numeric, String, Date, Enum
from . import Base


class StockProfile(Base):
    """ Model for stock basic infomations. """

    __tablename__ = 'stock_profile'

    ticker = Column(String(6), primary_key=True)
    pinyin = Column(String(16))

    short_name = Column(String(16), nullable=False, unique=True)
    full_name = Column(String(32))

    listing_date = Column(Date)
    listing_status = Column(String(2))

    shares_outstanding = Column(Integer)
    shares_tradable = Column(Integer)

    PE = Column(Numeric(precision=10, scale=2))
    PB = Column(Numeric(precision=10, scale=2))
    EPS = Column(Numeric(precision=10, scale=2))
    ROE = Column(Numeric(precision=10, scale=4))

    revenue = Column(Integer)
    revenue_growth = Column(Numeric(precision=4, scale=4))
    net_income = Column(Integer)
    net_income_growth = Column(Numeric(precision=4, scale=4))
