# -*- coding: utf-8 -*-

from lxml import etree
import re, os
pages = os.listdir("./page6")
from collections import defaultdict

page_sum = 0
for ind, i in enumerate(pages):

    file = "./page6/"+str(i)
    with open(file, encoding="utf-8", mode='r') as f:
        txt = f.read()

    txt = etree.HTML(txt)
    style = txt.xpath('//style[1]/text()')
    styles = defaultdict()
    style = style[0].split("\n")
    style = [i.strip() for i in style]
    for i in style:
        keys = re.split(r'[{}:""]', i)
        if "margin-right:"in i:
            styles[keys[0][1:].strip()] = ("margin-right", 0)
        elif "left:" in i:
            styles[keys[0][1:].strip()] = ("left", int(keys[-2][:-3]))
        elif "content:" in i:
            styles[keys[0][1:].strip()] = ("content", int(keys[-3]))

    css = txt.xpath('//div[@class="row"]/div[@class="col-md-1"]//@class')[::-1]
    num = txt.xpath('//div[@class="row"]/div[@class="col-md-1"]//text()')
    num = [int(i) for i in num if i.strip()]
    index = 0
    num_i = 0
    sum_nums = []
    for i in css:
        if i != "col-md-1":
            index = index+1
            if i in styles.keys():
                key, k = styles[i]
            else:
                key, k = i, 0
            if key !="content":
                value = num.pop()
                if k <=10 and key != "margin-right":
                    num_i += value * 10 ** (index - k - 1)
                # elif k==1:
                #     num_i += value * 10 ** (index - 1)
            else:
                num_i = k

        else:
            sum_nums.append(num_i)
            index = 0
            num_i = 0
    page_sum += sum(sum_nums)
    print("读取第 %d 个网页, params:%s" %(ind,file))

print(page_sum)