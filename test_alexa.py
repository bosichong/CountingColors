#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

Chinaz，世界网站排名
https://alexa.chinaz.com/Global/index.html

采集排名前100

'''
###### Sun Jan 31 18:13:04 CST 2021
import CountingColors  # 引入采集助手包

def main():
# 因为要采集的列表不是很多，手动组装了网址列表
    urllist = [
        "https://alexa.chinaz.com/Global/index.html",
        "https://alexa.chinaz.com/Global/index_2.html",
        "https://alexa.chinaz.com/Global/index_3.html",
        "https://alexa.chinaz.com/Global/index_4.html",
    ]

    for url in urllist:
        bf = CountingColors.getBf(url)
        ulbf = bf.find(name="ul", attrs={"class": "rowlist"})  # 定位数据位置
        li_list = ulbf.find_all(name="li", attrs={"class": "clearfix"})
        for li in li_list:  # 再次循环输出处理每一条网站数据
            alexacount = li.find(name="div", attrs={"class": "count"}).string  # 网站排名
            sitename = li.find(name="span").string#网站名称
            siteinfo = li.find(name="p").string#网站简介
            #网站URL
            #由于出现个别URL的缺失，这里抛出错误后修正URL
            try:
                siteurl = li.find(name="a", attrs={"class": "tohome"}).get("href")
            except:
                siteurl = sitename
            print("{} {} {}".format(alexacount, sitename, siteurl,))
            print(siteinfo)
if __name__ == '__main__':
    main()