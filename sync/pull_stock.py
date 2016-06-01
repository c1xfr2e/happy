# coding: utf-8

import logging
from crawler.eastmoney.stock_profile import fetch_stock_profile
from db.mongo import client
from models import Session


def pull_stock_profile(stock_codes):
    session = Session()
    failed_codes = []

    for code in stock_codes:
        try:
            stock = fetch_stock_profile(code)
            session.merge(stock)
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
    codes = [_['code'] for _ in client.alchemist.stock_codes.find()]
    pull_stock_profile(codes)
