# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql://root@localhost/alchemist")
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)

from stock import Stock
