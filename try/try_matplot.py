# coding: utf-8

from decimal import Decimal
from models import HQ, Session, HSIndex

import matplotlib
matplotlib.use('WXAgg')
from matplotlib import pyplot as plt


s = Session()
hqs = s.query(HQ).filter(HQ.code == '399006').order_by(HQ.from_date.desc()).limit(10).all()
hqs.reverse()
closes = [float(hq.close.quantize(Decimal('.01'))) for hq in hqs]
dates = [hq.from_date for hq in hqs]

plt.plot(dates, closes, color='blue', marker='o', linestyle='solid')
plt.title('399006')
plt.ylabel('close')
plt.grid(True, color='k')
plt.show()
