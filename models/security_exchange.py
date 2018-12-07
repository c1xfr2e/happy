# coding: utf-8

from sqlalchemy import Column, String
from . import Base


class SecurityExchange(Base):
    __tablename__ = 'security_exchange'

    id = Column(String(16), primary_key=True)
    code = Column(String(10))
    alias_code = Column(String(10))
    name = Column(String(16))
