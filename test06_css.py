# -*- coding: utf-8 -*-
import requests
import re, os
import threading
from lxml import etree
import time

url = 'http://glidedsky.com/login'

h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
}

session = requests.session()

session.headers = h

token = session.get(url)

_token = re.search(r'name="_token" value="(.*?)"', token.text).group(1)

print(_token)
data = {
    "_token": _token,
    "email": "760855003@qq.com",
    "password": "5vVYfr9sED5Dcux",
}

res = session.post(url, data=data, )

# xpath

def savePage(page, html):
    with open(r'.\page6\\' + str(page) + '.txt', 'w') as f:
        f.write(html.text)


page = os.listdir("./page6")
pages = [i for i in range(1, 1001) if str(i)+".txt" not in page]
print(len(pages))

def downloadPage(i):
    url = "http://glidedsky.com/level/web/crawler-css-puzzle-1?page="+str(i)
    html = session.get(url)
    if html.status_code==200:
        savePage(i, html)
        print("成功:{}".format(i))
    else:
        # pages.append(i)
        print("失败:{}".format(i))


while len(pages) > 0:
    for i in range(0, 5):
        i = pages.pop(0)
        t = threading.Thread(target=downloadPage, args=(i,))
        t.start()
    time.sleep(1)



# txt = etree.HTML(res2.text)
# print(res2.text)
