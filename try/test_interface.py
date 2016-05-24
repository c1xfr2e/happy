
import requests

url = 'http://www.szse.cn/szseWeb/FrontController.szse?randnum=0.8113631247765125'
data = {
    'ACTIONID': 3,
    'ISAJAXLOAD': True,
    'CATALOGID': 'mainzshq',
    'code': 399006
}

resp = requests.post(url, data=data)
print resp.content
