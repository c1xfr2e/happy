# coding: utf8

from sqlalchemy import Column, Integer, Numeric, String, Date
from . import Base


class StockFinance(Base):
    __tablename__ = 'stock_finance'
