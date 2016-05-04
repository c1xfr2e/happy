# coding: utf-8

from sqlalchemy import create_engine, inspect
from models import engine, Base, Session
# from models.stock import Stock

Base.metadata.create_all()
insp = inspect(engine)
print insp.get_table_names()
print insp.get_columns("Stock")
print insp.get_primary_keys("Stock")
print insp.get_schema_names()
