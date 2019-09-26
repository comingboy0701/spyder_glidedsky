# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 13:08:56 2018

@author: CHENKM2
"""

import requests
from multiprocessing.dummy import Pool as ThreadPool # 引入这个库来获得map函数的并发版本

#设置全局变量，来保存可用的 IP
alive_ip = []

def validate(ip):
   IP = {'http':ip} #指定对应的 IP 进行访问网址
   try:
       r = requests.get('http://www.baidu.com', proxies=IP, timeout=3)# proxies 设定对应的代理 IP 进行访问， timeout 设定相应的时间之后停止等待响应
       if r.status_code == 200:
           print("成功:{}".format(ip))
           alive_ip.append(ip) # 有效的 IP 则添加进去
   except:
       print("无效")

def save():
   with open(r'.\ip.txt','a+') as f: # 将有效的 IP 写入文件中保存
       for ip in alive_ip:
           f.write(ip+'\n')
           print(ip)
       print("成功保存所有有效 ip ")

def main():
   with open(r'.\456.txt','r') as f:
       lines = f.readlines()
       # 我们去掉lines每一项后面的\n\r之类的空格
       # 生成一个新的列表！
       ips = list(map(lambda x:x.strip(),[line for line in lines]))# strip() 方法用于移除字符串头尾指定的字符，默认就是空格或换行符。  
       pool = ThreadPool(20) # 多线程 设置并发数量！
       pool.map(validate, ips) # 用 map 简捷实现 Python 程序并行化
       save() # 保存能用的 IP

if __name__ == "__main__":
   main()