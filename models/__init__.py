# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://root@localhost/alchemist')
# Base.metadata.bind = engine
# Session = sessionmaker(bind=engine)

from stock_profile import StockProfile
from hq_snapshot import HQSnapshot

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

snapshot = HQSnapshot(
    code='399006',
    name=u'创业板指',
    date='20160517',
    time='15:00',
    price=2022.38,
    volume=1000000
)
session.add(snapshot)
session.commit()

hq_snapshots = session.query(HQSnapshot).filter(HQSnapshot.code=='399006').all()
for hq in hq_snapshots:
    print hq
