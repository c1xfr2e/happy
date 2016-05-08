
from crawler.stock_deatil import fetch_stock_profile
from db.mongo import client

codes_objs = client.alchemist.stock_codes.find(
    { 'status': {'$ne': 'fetch_profile_succeed'}}
)
stock_codes = [_['code'] for _ in codes_objs]

failed_codes = []

for code in stock_codes:
    try:
        stock_profile = fetch_stock_profile(code)
    except Exception as e:
        print code, e
        failed_codes.append(code)
        continue

    c_stock_profiles = client.alchemist.stock_profile
    result = c_stock_profiles.update(
        {'code': code},
        stock_profile,
        upsert=True
    )
    print result
    client.alchemist.stock_codes.update(
        {'code': code},
        {'$set': {'status': 'fetch_profile_succeed'}}
    )

result = client.alchemist.stock_codes.update(
    {'codes': {'$in': failed_codes}},
    {'$set': {'status': 'fetch_profile_failed'}},
    multi=True
)
print result
