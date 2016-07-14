# coding: utf-8

import logging
from crawler.eastmoney.stock_profile import fetch_stock_profile
from models import Session


def update_stock_profile(stock_codes):
    session = Session()
    failed_codes = []

    for code in stock_codes:
        try:
            stock = fetch_stock_profile(code)
            session.merge(stock)
            session.commit()
        except Exception as e:
            logging.warning('%s: %s' % (code, e))
            failed_codes.append(code)
            continue

    if failed_codes:
        update_stock_profile(failed_codes)


if __name__ == '__main__':
    codes = ['300342']
    update_stock_profile(codes)
