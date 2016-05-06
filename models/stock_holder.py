# coding: utf-8

from sqlalchemy import Column, Integer, Numeric, String, Date
from . import Base


class ShareHolder(Base):
    __tablename__ = 'shareholder'

    reporting_term = Column(Date, nullable=False)
    holder_name = Column(String(64), nullable=False)
    holder_type = Column(String(16))
    holding_shares = Column(Integer, nullable=False)
    shares_type = Column(String(16))
    holding_percentage = Column(Numeric(precision=4, scale=4))
    change_amount = Column(Integer)
    change_percentage = Column(Numeric(precision=4, scale=4))
