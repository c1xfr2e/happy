# coding: utf-8

import requests
from bs4 import BeautifulSoup


url = 'http://quote.eastmoney.com/sz300342.html'
r = requests.get(url)
soup = BeautifulSoup(r.content)


