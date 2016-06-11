# coding: utf-8

from decimal import Decimal
import numpy
import talib
from models import Session, Quote

s = Session()
hqs = s.query(Quote).filter(Quote.code=='399006').order_by(Quote.datetime.desc()).limit(50).all()
hqs.reverse()

# TODO: Decimal with 3 places roundup to 2.
close_list = [float(hq.close.quantize(Decimal('.01'))) for hq in hqs]
print close_list

close_arr = numpy.asarray(close_list)
ma5 = talib.SMA(close_arr, timeperiod=5)
print ma5
