# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from . import Base


class Stock(Base):
    """ Model for stock basic infomations. """

    __tablename__ = 'stock'

    id = Column(String, primary_key=True)
    ticker = Column(String, nullable=False, unique=True)
    short_name = Column(String, nullable=False, unique=True)
    full_name = Column(String)
    pinyin = Column(String)
    listing_date = Column(Date)
    listing_status = Column(String)
    shares_outstanding = Column(Integer)
    shares_tradable = Column(Integer)

    # revenue = Column(Integer)
    # net_income = Integer()
    # operating_income = Column(Integer)
