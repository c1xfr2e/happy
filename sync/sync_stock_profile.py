# coding: utf-8

import logging
from config import log_format
from crawler.stock_deatil import fetch_stock_profile
from db.mongo import client

logging.basicConfig(format=log_format)


def sync_stock_profiles():
    codes_objs = client.alchemist.stock_codes.find()  # {'status': {'$ne': 'fetch_profile_succeed'}}
    stock_codes = [_['code'] for _ in codes_objs]

    failed_codes = []

    for code in stock_codes:
        try:
            stock_profile = fetch_stock_profile(code)
        except Exception as e:
            logging.warning('%s: %s'%(code, e))
            failed_codes.append(code)
            continue

        c_stock_profiles = client.alchemist.stock_profile
        result = c_stock_profiles.update(
            {'code': code},
            stock_profile,
            upsert=True
        )
        logging.info('%s: %s'%(code, result))
        client.alchemist.stock_codes.update(
            {'code': code},
            {'$set': {'status': 'fetch_profile_succeed'}}
        )

    result = client.alchemist.stock_codes.update(
        {'code': {'$in': failed_codes}},
        {'$set': {'status': 'fetch_profile_failed'}},
        multi=True
    )
    logging.info(result)


if __name__ == '__main__':
    sync_stock_profiles()
