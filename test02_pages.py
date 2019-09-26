# -*- coding: utf-8 -*-

import requests

import re

from lxml import etree

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
# 第二关 url
url ="http://glidedsky.com/level/web/crawler-basic-2?page= "
nums = 0
for i in range(1,2):
    print("scrapy: page %d" %i)
    url_i = url+str(i)
    res2 = session.get(url_i)
    txt = etree.HTML(res2.text)

    num_i = txt.xpath("//div[@class='col-md-1']/text()")

    num_i = list(map(lambda x:int(x.strip()), num_i))
    print(num_i)
    nums += sum(num_i)


