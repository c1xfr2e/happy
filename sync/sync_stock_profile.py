
from crawler.stock_deatil import fetch_stock_profile
from db import db_conn
from db.mongo import client


cursor = db_conn.cursor()
sql = 'select * from hs_ticker'
stock_codes = []
try:
    cursor.execute(sql)
    stock_codes = [_[0] for _ in cursor.fetchall()]
except Exception as e:
    print 'select error', e

bad_codes = []

for code in stock_codes:
    stock_profile = fetch_stock_profile(code)

    if not stock_profile:
        bad_codes.append(code)
        continue

    c_stock_profiles = client.alchemist.stock_profile
    result = c_stock_profiles.update(
        { 'code': code },
        stock_profile,
        upsert=True
    )
    print result
