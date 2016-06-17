# coding: utf-8

import requests
from bs4 import BeautifulSoup

# eastmoney url
url = 'http://f10.eastmoney.com/f10_v2/BonusFinancing.aspx?code=sh601377'


def fetch_exdiv_history(code):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
