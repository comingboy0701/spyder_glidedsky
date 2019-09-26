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
# 第一关 url

# xpath
res2 = session.get('http://glidedsky.com/level/web/crawler-basic-1')
txt = etree.HTML(res2.text)
nums1 = txt.xpath("//div[@class='col-md-1']/text()")
nums1 = list(map(lambda x:int(x.strip()), nums1))
print(sum(nums1))

# 正则
html = re.search(r'<div class="row">(.*)</main>', res2.text, re.S)
nums2 = re.findall(r'\d{3}', html.group(1))
nums2 = list(map(lambda x:int(x.strip()), nums2))
print(sum(nums2))


