# coding: utf-8

"""
Fetch realtime index and stock quotes at eastmoney.com.

Index page URLs:
    上证指数 SSE Composite Index (000001.SS)  http://quote.eastmoney.com/zs000001.html
    深圳成指 SZSE COMP SUB IND (399001.SZ)    http://quote.eastmoney.com/zs399001.html
    创业板指 SZSE ChiNext (399006.SZ)         http://quote.eastmoney.com/zs399006.html
    沪深300 CSI 300 Index (000300.SS)        http://quote.eastmoney.com/zs000300.html
    上证50  SSE 50 Index (000016.SS)         http://quote.eastmoney.com/zs000016.html
    中证500 CSI 500 Index (000905.SS)        http://quote.eastmoney.com/zs000905.html

Stock page URLs:
    600000  浦发银行  http://quote.eastmoney.com/sh600000.html
    300342  天银机电  http://quote.eastmoney.com/sz300342.html

HTML element section as bellow:
    <div class="qphox layout mb7">
        <div class="fl xt1 data-left">
            <div id="arrowud" xid="0" class="red">
                <span class="ar a">
                    <strong id="price9" class="xp1" style="">2837.04</strong>
                    <i id="arrow-find" class="xp2 up-arrow"></i>
                </span>
                <span class="ar b">
                    <b id="km1" class="xp3" style="">4.45</b>
                    <b id="km2" class="xp4" style="">0.16%</b>
                </span>
            </div>
        </div>
        <div class="data-middle">
            <table cellspacing="0" cellpadding="0" class="yfw">
                <tbody>
                    <tr>
                        <td>今开：</td><td id="gt1" class="txtl red">2843.55</td>
                        <td>最高：</td><td id="gt2" class="txtl red">2857.25</td>
                        <td>涨跌幅：</td><td id="gt3" class="txtl red">0.16%</td>
                        <td>换手：</td><td id="gt4" class="txtl">0.49%</td>
                        <td>成交量：</td><td id="gt5" class="txtl">13580万手</td>
                    </tr>
                    <tr>
                        <td>昨收：</td><td id="gt7" class="txtl">2832.59</td>
                        <td>最低：</td><td id="gt8" class="txtl green">2818.70</td>
                        <td>涨跌额：</td><td id="gt9" class="txtl red">4.45</td>
                        <td>振幅：</td><td id="gt10" class="txtl">1.36%</td>
                        <td>成交额：</td><td id="gt11" class="txtl">1460亿元</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

But all the real data is filled by javascript functions.
The javascript code is at: http://hqres.eastmoney.com/EM15AGIndex/js/quote-min.js
See the function 'DisQuote' in the above javascript code to guess what's this!

HTTP interface for index and stock quote data:
    index 000001  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0000011
    index 000300  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0003001
    index 399001  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990012
    index 399006  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990062
    stock 600000  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=6000001
    stock 300342  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3003422

The 'id' is code+'1' for ShangHai market and code+'2' for ShenZhen market.

And what they return is like:
    callback({
        "Comment": [],
        "Value": [...]
    })

Sample of 'Value' list:
    Value = [
        "1",  # [0] 1:上海 2:深圳
        "600597",  # [1]
        "光明乳业",  # [2]
        "12.64", "12.63", "12.62", "12.61", "12.60",  # [3,7] 买一至买五
        "12.65", "12.66", "12.68", "12.69", "12.70",  # [8,12] 卖一至卖五
        "8","79","50","61","471",  # [13,17] 买一至买五挂单数
        "6","265","387","28","401",  # [18,22] 卖一至卖五挂单数
        "14.49",  # [23] 涨停价
        "11.85",  # [24] 跌停价
        "12.67",  # [25] 最新
        "12.82",  # [26] 均价
        "-0.50",  # [27] 涨跌值
        "13.14",  # [28] 开盘价
        "-3.80",  # [29] 涨跌比例
        "13.14",  # [30] 最高价
        "192669",  # [31] 成交手数
        "12.54",  # [32] 最低价
        "6",      # [33]
        "13.17",  # [34] 前日收盘价
        "2.47亿",  # [35] 成交金额
        "0.85",  # [36] 量比
        "1.57",  # [37] 换手率
        "32.99",  # [38] 市盈率
        "71552",  # [39] 外盘
        "121117",  # [40] 内盘
        "-23.78",  # [41] 委比
        "-418",  # [42] 委差
        "3.33",  # [43] 市净率
        "1",  # [44]
        "15511907447",  # [45] 流通市值
        "15592167577",  # [46] 总市值
        "0|0|0|0|0",  # [47]
        "0|0|0|0|0",  # [48]
        "2016-05-13 15:23:51",  # [49]
        "4.56",  # [50]
        "-",
        "-"
    ]

"""

from collections import OrderedDict
import re
import json
import requests
from util import stock_market

"""
code: stock or index code
market: 1-SH 2-SZ
Sample:
    000001  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0000011
    600000  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=6000001
    300342  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3003422
"""
quote_url = 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id={code}{market}'


def fetch_stock_quote(code):
    market = stock_market(code)
    market_code = '1' if market == 'sh' else '2'
    url = quote_url.format(code=code, market=market_code)

    resp = requests.get(url)
    data_text = re.findall('callback\((.*)\)', resp.content)[0]
    data = json.loads(data_text)
    values = data['Value']

    keys = [
        "market_code",  # [0] 1:上海 2:深圳
        "code",  # [1]
        "name",  # [2]
        "bid_1_price", "bid_2_price", "bid_3_price", "bid_4_price", "bid_5_price",  # [3,7] 买一至买五
        "ask_1_price", "ask_2_price", "ask_3_price", "ask_4_price", "ask_5_price",  # [8,12] 卖一至卖五
        "bid_1_size","bid_2_size","bid_3_size","bid_4_size","bid_5_size",  # [13,17] 买一至买五挂单数
        "ask_1_size","ask_2_size","ask_3_size","ask_4_size","ask_5_size",  # [18,22] 卖一至卖五挂单数
        "limit_up_price",  # [23] 涨停价
        "limit_down_price",  # [24] 跌停价
        "current_price",  # [25] 最新
        "average_price",  # [26] 均价
        "change",  # [27] 涨跌值
        "open",  # [28] 开盘价
        "change_ratio",  # [29] 涨跌比例
        "high",  # [30] 最高价
        "volume_size",  # [31] 成交手数
        "low",  # [32] 最低价
        "_",      # [33]
        "pre_close",  # [34] 前日收盘价
        "volume_amount",  # [35] 成交金额
        "minute_volume_ratio",  # [36] 量比
        "turnover_rate",  # [37] 换手率
        "pe",  # [38] 市盈率
        "out_size",  # [39] 外盘
        "in_size",  # [40] 内盘
        "bid_ask_ratio",  # [41] 委比
        "bid_ask_diff",  # [42] 委差
        "pb",  # [43] 市净率
        "_",  # [44]
        "circulated_market_value",  # [45] 流通市值
        "total_market_value",  # [46] 总市值
        "_",  # [47]
        "_",  # [48]
        "datetime",  # [49]
        "_",  # [50]
        "_",
        "_"
    ]

    quote = OrderedDict(zip(keys, values))
    return quote
