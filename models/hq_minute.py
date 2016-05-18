# coding: utf-8

from sqlalchemy import BigInteger, Column, Date, Numeric, String, Time, UniqueConstraint
from . import Base


class HQMinute(Base):
    __tablename__ = 'hq_minute'

    code = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    time = Column(Time, primary_key=True)

    price = Column(Numeric(precision=10, scale=2), nullable=False)
    volume = Column(BigInteger, nullable=False)
    volume_money = Column(BigInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint('code', 'date', 'time', name='hq_minute_code_date_time'),
    )
