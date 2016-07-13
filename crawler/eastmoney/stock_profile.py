# coding: utf-8

from datetime import datetime
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
from crawler.util import cntext_to_number, cntext_to_int
from models import Stock


'''
    东方财富个股首页 股票基本信息:
        收益(一) 0.210
        PE(动) 18.74
        净资产 5.355
        市净率 2.94
        收入 53.00亿
        同比 16.85%
        净利润 4.44亿
        同比 -5.78%
        毛利率 27.00%
        净利率 10.28%
        ROE 3.76%
        负债率 69.54%
        总股本 21.62亿
        总值 340.4亿
        流通股 21.62亿
        流值 340.4亿
        每股未分配利润 3.402元
        上市时间 2001-01-05
'''


stock_page_url = 'http://quote.eastmoney.com/{market}{stock_code}.html'


def value_or_zero(data, function, zero=0):
    try:
        return function(data)
    except:
        return zero


def fetch_stock_profile(stock_code):
    market = 'sh' if stock_code.startswith('6') else 'sz'
    url = stock_page_url.format(market=market, stock_code=stock_code)
    r = requests.get(url)
    soup = BeautifulSoup(r.content.decode('gbk'))

    name_elem = soup.find('h2', id='name')
    stock_name = name_elem.text if name_elem else None

    # last_price = soup.find('strong', id='price9').text

    status = 'L'

    '''
        上市状态
            上市: L
            退市: DE
        dead_status = [u'已退市', u'终止上市']
        stop_status = [u'暂停上市']
        if stock_name in dead_status:
            status = 'DE'
        elif stock_name in stop_status:
            status = 'S'
    '''

    texts = []
    trs = soup.find('table', id='rtp2').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        for td in tds:
            texts.append(td.text.split(u'：'))

    datas = {_[0]: _[1] for _ in texts}

    eps = value_or_zero(datas.get(u'收益(一)'), Decimal)
    if eps == 0:
        eps = value_or_zero(datas.get(u'收益'), Decimal)

    pe = value_or_zero(datas.get(u'PE(动)'), Decimal)
    asset_value_per_share = value_or_zero(datas.get(u'净资产'), Decimal)
    pb = value_or_zero(datas.get(u'净利率'), cntext_to_number)
    revenue = value_or_zero(datas.get(u'总收入'), cntext_to_int)
    revenue_growth = value_or_zero(texts[5][1], cntext_to_number)
    net_profit = value_or_zero(datas.get(u'净利润'), cntext_to_number)
    net_profit_growth = value_or_zero(texts[7][1], cntext_to_number)
    roe = value_or_zero(datas.get(u'ROE'), cntext_to_number)
    outstanding_shares = value_or_zero(datas.get(u'总股本'), cntext_to_int)
    tradable_shares = value_or_zero(datas.get(u'流通股'), cntext_to_int)
    market_value=value_or_zero(datas.get(u'总值'), cntext_to_number)
    circulating_value=value_or_zero(datas.get(u'流值'), cntext_to_number)
    retained_earnings_per_share = value_or_zero(datas.get(u'每股未分配利润'), cntext_to_number)
    debt_ratio = value_or_zero(datas.get(u'负债率'), cntext_to_number)
    listing_date_str = value_or_zero(datas.get(u'上市时间'), str, zero='-')
    gross_profit_margin = value_or_zero(datas.get(u'毛利率'), cntext_to_number)
    if listing_date_str != '-':
        listing_date = datetime.strptime(listing_date_str, '%Y-%m-%d').date()
    else:
        listing_date = '-'

    stock = Stock(
        market=market,
        code=stock_code,
        status=status,
        listing_date=listing_date,
        outstanding_shares=outstanding_shares,
        tradable_shares=tradable_shares,
        market_value=market_value,
        circulating_value=circulating_value,
        revenue=revenue,
        revenue_growth=revenue_growth,
        net_profit=net_profit,
        net_profit_growth=net_profit_growth,
        asset_value_per_share=asset_value_per_share,
        retained_earnings_per_share=retained_earnings_per_share,
        debt_ratio=debt_ratio,
        gross_profit_margin=gross_profit_margin,
        pe=pe,
        pb=pb,
        eps=eps,
        roe=roe,
        update_time=datetime.now()
    )

    if stock_name:
        stock.name = stock_name

    return stock


if __name__ == '__main__':
    try:
        stock = fetch_stock_profile('600666')
        print stock
    except Exception as e:
        import os, sys, traceback
        exc_info = sys.exc_info()
        s = traceback.format_exception(*exc_info)
        del exc_info
