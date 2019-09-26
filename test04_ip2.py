# -*- coding: utf-8 -*-

import requests
import os
import re
from multiprocessing.dummy import Pool as ThreadPool
from lxml import etree
import threading
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

url = "http://glidedsky.com/level/web/crawler-ip-block-2?page="

def page_add(i):
    lock.acquire()
    if i not in pages:
        pages.append(i)
        print("失败:{},剩余{}".format(i, len(pages)))
    lock.release()

def IP():
# 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HDZ955Y3Z33IX92D"
    proxyPass = "F889319E51D5EE0B"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }

    return proxies

def validate(i):

    url_i = url+str(i)
    try:
       r = session.get(url_i, proxies=IP(), timeout=2)# //,proxies 设定对应的代理 IP 进行访问， timeout 设定相应的时间之后停止等待响应
       if r.status_code == 200:
           txt = etree.HTML(r.text)
           num_i = txt.xpath("//div[@class='col-md-1']/text()")
           num_i = list(map(lambda x: int(x.strip()), num_i))
           if len(num_i)>0:
               with open(r'.\page2\\' + str(i), 'w') as f:
                   f.write(r.text)
               print(num_i)
               print("成功:{}".format(i))
           else:
               page_add(i)
       else:
           page_add(i)
    except:
        page_add(i)

# 第四关 ip

lock = threading.Lock()

page = os.listdir("./page2")
pages = [i for i in range(1, 1001) if str(i) not in page]
print(len(pages))

# pool = ThreadPool(5) # 多线程 设置并发数量！
# pool.map(validate, pages) # 用 map 简捷实现 Python 程序并行化

while len(pages) > 0:
    for i in range(0, 5):
        if len(pages) > 0:
            i = pages.pop()
            t = threading.Thread(target=validate, args=(i,))
    t.start()
    time.sleep(1)

num = 0
page = os.listdir("./page2")
for i in page:
    with open(r'.\page2\\' + str(i), 'r') as f:
        txt = f.read()
        txt = etree.HTML(txt)
        num_i = txt.xpath("//div[@class='col-md-1']/text()")
        num_i = list(map(lambda x: int(x.strip()), num_i))
    print(sum(num_i))
    num+=sum(num_i)
print(num)