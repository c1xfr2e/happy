# coding: utf-8

import requests
from bs4 import BeautifulSoup

'''
    十大(流通)股东 局部页面结构
    <div class="section">
        <div class="name" id="sdltgd">
            <strong>十大流通股东</strong>
        </div>
        <div class="content">
            <div class="tab">
                <ul>
                    <li> <span>2016-03-31</span> </li>
                    <li> <span>2015-12-31</span> </li>
                    <li> <span>2015-09-30</span> </li>
                    <li> <span>2015-06-30</span> </li>
                    <li> <span>2015-03-31</span> </li>
                </ul>
            </div>
            <div class="content first" id="TTCS_Table_Div">
                <table />
                    <tr>
                        <th class="tips-colnameL" width="5%">名次</th>
                        <th class="tips-colnameL">股东名称</th>
                        <th class="tips-colnameL" width="14%">股东性质</th>
                        <th class="tips-colnameL" width="8%">股份类型</th>
                        <th class="tips-colnameL" width="12%">持股数(股)</th>
                        <th class="tips-colnameL" width="9%">占总流通股本持股比例</th>
                        <th class="tips-colnameL" width="10%">增减(股)</th>
                        <th class="tips-colnameL" width="8%">变动比例</th>
                    </tr>
                    <tr>
                        <th class="tips-dataL"><em class="tips-num">1</em></th>
                        <td class="tips-dataL">常熟市天恒投资管理有限公司</td>
                        <td class="tips-dataL">投资公司</td>
                        <td class="tips-dataL">A股</td>
                        <td class="tips-dataL">100,125,000</td>
                        <td class="tips-dataL">52.98%</td>
                        <td class="tips-dataL">不变</td>
                        <td class="tips-dataL">--</td>
                    </tr>
                    <tr> ... </tr>
                    ...
                <table> ... </>
                <table> ... </>
                <table> ... </>
                <table> ... </>
            </div>
        </div>
    </div>
'''

params = {
    'top_shareholders': {
        'content_table_div_id': 'TTCS_Table_Div'
    },
    'top_tradable_shareholders': {
        'content_table_div_id': 'TTS_Table_Div'
    }
}

url = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=sh601318'
r = requests.get(url)
soup = BeautifulSoup(r.content)

top_tradable_shareholders_root = soup.find(id='sdltgd').parent
tab_of_date = top_tradable_shareholders_root.find(class_='tab')
date_lis = tab_of_date.find_all('li')
date_count = len(date_lis)

records_root = top_tradable_shareholders_root.find(id='TTCS_Table_Div')
records_tables = records_root.find_all('table')
for date_li, record_table in zip(date_lis, records_tables):
    print(date_li.text)
    trs = record_table.find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        for td in tds:
            print(td.text, end=' ')
        print()


def eastmoney_top_shareholders(ticker, tradable):
    pass
