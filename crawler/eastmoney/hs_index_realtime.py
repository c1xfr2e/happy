# coding: utf-8

"""
Fetch current index quotes at eastmoney.com:

    上证指数 SSE Composite Index (000001.SS)  http://quote.eastmoney.com/zs000001.html
    深圳成指 SZSE COMP SUB IND (399001.SZ)    http://quote.eastmoney.com/zs399001.html
    创业板指 SZSE ChiNext (399006.SZ)         http://quote.eastmoney.com/zs399006.html
    沪深300 CSI 300 Index (000300.SS)        http://quote.eastmoney.com/zs000300.html
    上证50  SSE 50 Index (000016.SS)         http://quote.eastmoney.com/zs000016.html
    中证500 CSI 500 Index (000905.SS)        http://quote.eastmoney.com/zs000905.html

HTML element section for 000001.SS is as below.

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

Data interface for index quote data:

    000001: http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0000011
    000300: http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0003001
    399001: http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990012
    399006: http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990062

And what they return is like:

    callback({
        "Comment": [],
        "Value": ["1","000001","上证指数","3120.74","2553.33","2835.86","10.33","-1.18",
                  "2812.11","-0.04","2839.28","136337656","2781.24","33285","2837.04",
                  "1408亿","43.88","0.49","-","68315461","68022195","0.00","0","0.00",
                  "1","20794444719483","28187506136335","0|0|0|0|0","0|0|0|0|0",
                  "2016-05-12 15:21:10","2.05","-","-"]
    })

See the function 'DisQuote' in the above javascript code to guess what's this!

"""

import re
import json
import requests


index_url = {
    '000001': 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0000011',
    '000300': 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0003001',
    '399001': 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990012',
    '399006': 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990062'
}


def fetch_index_profile(index_code):
    url = index_url.get(index_code)
    if not url:
        return None
    resp = requests.get(url)
    usefull_text = re.findall('callback\((.*)\)', resp.content)[0]
    obj = json.loads(usefull_text)
    values = obj['Value']

    current_price = values[25]
    changed_value = values[27]
    changed_percent = values[29]

    pre_close = values[34]
    open = values[28]
    high = values[30]
    low = values[32]

    turnover = values[37]
    volume = values[31]
    amount_money = values[35]
    time = values[49]

    print current_price, changed_value, changed_percent, high, low, turnover, amount_money
