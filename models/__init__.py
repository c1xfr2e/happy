# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("mysql://root@localhost/alchemist")
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)

from stock_profile import StockProfile
