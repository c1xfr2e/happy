# coding: utf-8

"""
Fetch current index quotes at eastmoney.com:

    上证指数 SSE Composite Index (000001.SS)  http://quote.eastmoney.com/zs000001.html
    深圳成指 SZSE COMP SUB IND (399001.SZ)    http://quote.eastmoney.com/zs399001.html
    创业板指 SZSE ChiNext (399006.SZ)         http://quote.eastmoney.com/zs399006.html
    沪深300 CSI 300 Index (000300.SS)        http://quote.eastmoney.com/zs000300.html
    上证50  SSE 50 Index (000016.SS)         http://quote.eastmoney.com/zs000016.html
    中证500 CSI 500 Index (000905.SS)        http://quote.eastmoney.com/zs000905.html

HTML element structure sample for http://quote.eastmoney.com/zs000001.html:

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

Data interface:
    上证指数: http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0000011
    沪深300: http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=0003001
    深圳成指: http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990012
    创业板:  http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id=3990062

    板块信息: http://data.eastmoney.com/bkzj/rank/hy/alljson.html

"""

import requests
from bs4 import BeautifulSoup


def fetch_index_profile(index_code):
    url = 'http://quote.eastmoney.com/zs{code}.html'.format(code=index_code)
    resp = requests.get(url)
    print resp.encoding
    soup = BeautifulSoup(resp.content)
    root = soup.find('div', class_='qphox layout mb7')

    price = root.find(id='price9').text
    change_value = root.find(id='km1').text
    change_percent = root.find(id='km2').text
    high = root.find(id='gt2').parent.text
    low = root.find(id='gt8').parent.text
    turnover = root.find(id='gt4').parent.text
    amount_money = root.find(id='gt11').parent.text

    print price, change_value, change_percent, high, low, turnover, amount_money
