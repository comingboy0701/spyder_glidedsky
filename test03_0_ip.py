# -*- coding: utf-8 -*-

import requests
import os
import re
from multiprocessing.dummy import Pool as ThreadPool
from lxml import etree
import threading

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

page = os.listdir("./page")
page_s = [i for i in range(1, 1001) if str(i) not in page]
print(len(page_s))

url ="http://glidedsky.com/level/web/crawler-ip-block-1?page="
def validate(ip):

    IP = {'http':ip} #指定对应的 IP 进行访问网址

    lock.acquire()
    i = page_s.pop(0)
    lock.release()

    url_i = url+str(i)
    try:
       r = session.get(url_i, proxies=IP, timeout=1)# //,proxies 设定对应的代理 IP 进行访问， timeout 设定相应的时间之后停止等待响应
       if r.status_code == 200:
           with open(r'.\page\\' + str(i), 'w') as f:
               f.write(r.text)

           txt = etree.HTML(r.text)
           num_i = txt.xpath("//div[@class='col-md-1']/text()")
           num_i = list(map(lambda x:int(x.strip()), num_i))
           print(num_i)
           print("成功:{}".format(i))
       else:
           lock.acquire()
           page_s.append(i)
           lock.release()
           print("失败:{},剩余{}".format(i, len(page_s)))
    except:
        lock.acquire()
        page_s.append(i)
        lock.release()
        print("失败:{},剩余{}".format(i, len(page_s)))

# 第三关 ip
with open(r'.\456.txt','r') as f:
   lines = f.readlines()
   # 我们去掉lines每一项后面的\n\r之类的空格
   # 生成一个新的列表！
   ips = list(map(lambda x: x.strip(), [line for line in lines]))


lock = threading.Lock()

print(len(ips))
pool = ThreadPool(50) # 多线程 设置并发数量！
pool.map(validate, ips) # 用 map 简捷实现 Python 程序并行化

