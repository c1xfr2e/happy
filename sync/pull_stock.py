# coding: utf-8

import logging
from config import log_format
from crawler.eastmoney.stock_profile import fetch_stock_profile
from db.mongo import client
from models import Session

logging.basicConfig(format=log_format)


def pull_all_stock_profile(codes=None):
    if codes:
        stock_codes = codes
    else:
        codes_objs = client.alchemist.stock_codes.find()  # {'status': {'$ne': 'fetch_profile_succeed'}}
        stock_codes = [_['code'] for _ in codes_objs]

    session = Session()
    failed_codes = []

    for code in stock_codes:
        try:
            stock = fetch_stock_profile(code)
            session.merge(stock)
            logging.warning(stock.code)
        except Exception as e:
            logging.warning('%s: %s' % (code, e))
            failed_codes.append(code)
            continue

    session.commit()

    client.alchemist.stock_codes.update(
        {'code': {'$in': failed_codes}},
        {'$set': {'status': 'fetch_profile_failed'}},
        multi=True
    )
    client.alchemist.stock_codes.update(
        {'code': {'$not': {'$in': failed_codes}}},
        {'$set': {'status': 'fetch_profile_done'}},
        multi=True
    )


if __name__ == '__main__':
    pull_all_stock_profile()
