# coding utf-8

from sqlalchemy import Column, Integer, String, Date, Time, Numeric
from . import Base


class HQSnapshot(Base):
    __tablename__ = 'hq_snapshot'

    id = Column(Integer, primary_key=True)
    code = Column(String(8), nullable=False)
    name = Column(String(16))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    volume = Column(Integer, nullable=False)
