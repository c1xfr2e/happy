# coding: utf-8

from sqlalchemy import Column, String, Date
from . import Base


class HSIndex(Base):
    __tablename__ = 'hs_index'

    id = Column(String(16), primary_key=True)
    market = Column(String(16), nullable=False)
    code = Column(String(10), nullable=False)
    name = Column(String(16), nullable=False)
    alias = Column(String(10))
    full_name = Column(String(32))
    listing_date = Column(Date)
