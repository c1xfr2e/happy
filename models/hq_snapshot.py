# coding utf-8

from sqlalchemy import Column, Integer, String, Date, Time, Numeric, BigInteger, UniqueConstraint
from . import Base


class HQSnapshot(Base):
    __tablename__ = 'hq_snapshot'

    code = Column(String(8), primary_key=True)
    date = Column(Date, primary_key=True)
    time = Column(Time, primary_key=True)
    name = Column(String(16))
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    change = Column(Numeric(precision=10, scale=2))
    change_percent = Column(Numeric(precision=4, scale=2))
    turnover = Column(Numeric(precision=4, scale=2))
    pre_close = Column(Numeric(precision=10, scale=2), nullable=False)
    open = Column(Numeric(precision=10, scale=2), nullable=False)
    high = Column(Numeric(precision=10, scale=2), nullable=False)
    low = Column(Numeric(precision=10, scale=2), nullable=False)
    volume = Column(BigInteger)
    volume_money = Column(BigInteger, nullable=False)

    __table_args__ = (
        UniqueConstraint('code', 'date', 'time', name='unique_code_date_time'),
    )
