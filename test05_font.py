# -*- coding: utf-8 -*-
from fontTools.ttLib import TTFont
from lxml import etree
import os

filename = r'./page5/3ZSEXG.woff'

def file_read(file,):
    with open(file, encoding="ufg", mode='r') as f:
        txt = f.read()
    return txt

sums_num = 0
sums_dict = dict()
page = list(filter(lambda x: x.endswith("txt"), os.listdir("./page5")))
page = list(map(lambda x: x[:-4], page))


for i in page:
    font_file = r'./page5/%s.woff' %str(i)

    font = TTFont(font_file)

    text_file = r'./page5/%s.txt' % str(i)

    with open(text_file, mode='r') as f:
        text = f.read()

    best_cmap = font['cmap'].getBestCmap()
    best_glpy = font['cmap'].tables[2].ttFont.getReverseGlyphMap()
    temp_cmap = dict()
    for key, value in best_cmap.items():
        temp_cmap[chr(key)] = value

    txt = etree.HTML(text)
    num_i = txt.xpath("//div[@class='col-md-1']/text()")
    num_i = list(map(lambda x: (x.strip()), num_i))

    nums = []
    num = ""
    for ns in num_i:
        for n in ns:
            num += str((best_glpy[temp_cmap[n]] - 2))
        nums.append(int(num))
        num = ""
    sums_dict[i] = nums


sum([sum(i) for i in sums_dict.values()])


# font.saveXML(filename.replace(filename.split('.')[-1], 'xml'))