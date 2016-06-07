# coding utf-8

from sqlalchemy import Column, Integer, String, Date, Time, Numeric, BigInteger, UniqueConstraint
from . import Base


class HQSnapshot(Base):
    __tablename__ = 'hq_snapshot'

    market = Column(String(16), primary_key=True)
    code = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    time = Column(Time, primary_key=True)
    name = Column(String(16))

    pre_close = Column(Numeric(precision=10, scale=3), nullable=False)
    open = Column(Numeric(precision=10, scale=3), nullable=False)
    high = Column(Numeric(precision=10, scale=3), nullable=False)
    low = Column(Numeric(precision=10, scale=3), nullable=False)

    price = Column(Numeric(precision=10, scale=3), nullable=False)
    change = Column(Numeric(precision=10, scale=3), nullable=False)
    percent = Column(Numeric(precision=8, scale=3), nullable=False)

    volume = Column(BigInteger, nullable=False)
    money = Column(BigInteger, nullable=False)

    turnover = Column(Numeric(precision=8, scale=2))

    __table_args__ = (
        UniqueConstraint('market', 'code', 'date', 'time', name='unique_hq_snapshot_mcdt'),
    )
