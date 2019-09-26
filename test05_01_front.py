# -*- coding: utf-8 -*-
import requests
import os
import re
from multiprocessing.dummy import Pool as ThreadPool
from lxml import etree
import threading
import time
class Sky_Main(object):
    def __init__(self):
        # 登录
        login_url = 'http://glidedsky.com/login'
        self.page_url = "http://glidedsky.com/level/web/crawler-font-puzzle-1?page="
        h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        }

        self.session = requests.session()
        self.session.headers = h
        token = self.session.get(login_url,)

        _token = re.search(r'name="_token" value="(.*?)"', token.text).group(1)

        data = {
            "_token": _token,
            "email": "760855003@qq.com",
            "password": "5vVYfr9sED5Dcux",
        }
        self.session.post(login_url, data=data, )

        page = list(filter(lambda x: x.endswith("txt"), os.listdir("./page5")))
        page = list(map(lambda x: x[:-4], page))
        self.pages = [i for i in range(1, 1001) if str(i) not in page]
        print(len(self.pages))
        self.sum_nums = 0
        self.lock = threading.Lock()

    def IP(self):
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

    def page_add(self, i):
        self.lock.acquire()
        if i not in self.pages:
            self.pages.append(i)
            print("失败:{},剩余{}".format(i, len(self.pages)))
        self.lock.release()

    def download_font(self, font_url, i):
        try:

            response = self.session.get(font_url)
            if response.status_code == 200:
                with open(r'.\page5\\' + str(i)+'.woff', 'wb') as f:
                    f.write(response.content)
                return True
            else:
                return False
        except:
            return False

    def get_page(self, i):
        url_i = self.page_url + str(i)
        try:
            r = self.session.get(url_i)  # //,proxies 设定对应的代理 IP 进行访问， timeout 设定相应的时间之后停止等待响应
            if r.status_code == 200:
                font_url = re.findall(r'src: url\("(.*?)"\)', r.text)
                font_stata = self.download_font(font_url[0], i)
                txt = etree.HTML(r.text)
                num_i = txt.xpath("//div[@class='col-md-1']/text()")
                num_i = list(map(lambda x: int(x.strip()), num_i))
                if len(num_i) > 0 and font_stata:
                    with open(r'.\page5\\' + str(i)+'.txt', 'w') as f:
                        f.write(r.text)
                    print(num_i)
                    print("成功:{}".format(i))
                else:
                    self.page_add(i)
            else:
                self.page_add(i)
        except:
            self.page_add(i)

    def run(self):
        while len(self.pages) > 0:
            max_l = min(3, len(self.pages))
            for i in range(0, max_l):
                i = self.pages.pop(0)
                self.get_page(i)
                # t = threading.Thread(target=self.get_page, args=(i,))
                # t.start()

            time.sleep(1)

if __name__ == '__main__':
    start = Sky_Main()
    start.run()


