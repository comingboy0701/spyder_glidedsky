# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 13:05:39 2018

@author: CHENKM2
"""
import requests
from lxml import etree
import time
from fake_useragent import UserAgent
import random
# 向网页请求数据，老套路了
def get_one_page(url):
   try:
       ua = UserAgent()
       headers = {'User-Agent': ua.random}
       reponse = requests.get(url, headers=headers, timeout=2)
       if reponse.status_code == 200:
           return reponse.text
       return None
   except:
       return None

def get_one_parse(url):
   with open(r'456.txt', 'a+') as f: # 保存在相应的文件里
       print(url) # 看爬取到第几页来了
       try:
           html = get_one_page(url)
           html = etree.HTML(html)# 从获得的html页面中分析提取出所需要的数据
           IP = html.xpath('.//*[@id="list"]/table/tbody//td[1]/text()') # 解析到相应的位置，用我上次教大家的方法，很方便的
           poots = html.xpath('.//*[@id="list"]/table/tbody//td[2]/text()')# 这是 端口位置
           for (ip, poot) in zip(IP, poots): # 保存
               ip = ip +':' +  poot
               print("测试：{}".format(ip))
               f.write(ip + '\n')
               #validate(ip)
       except:
           pass


url = 'https://www.kuaidaili.com/free/intr/{}/' # 这是网站的 url
for i in range(200, 500): # 爬取二十页
    timewait = random.random()*2
    time.sleep(timewait)  # 休息 1 秒
    get_one_parse(url.format(i))