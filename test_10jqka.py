#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

同花顺龙虎榜
http://data.10jqka.com.cn/market/longhu/

采集今日营业部排名前20

'''

import CountingColors
def main():
    url = "http://data.10jqka.com.cn/market/longhu/"#需要采集的网址
    bf = CountingColors.getBf(url)#获取bs4对象
    yybdiv = bf.find(name="div",attrs={"class":"yyb"}).table.tbody#搜索数据的table
    trlist = yybdiv.find_all(name="tr",)#采集table内的数据
    for tds in trlist:    #循环打印出需要采集的数据。
        tdlist = tds.find_all(name="td")
        k = 0
        for td in tdlist:
            if k != 1 :
                print("{} ".format(td.text),end="")
            else:
                print("{} ".format(td.a["title"]),end="")
            k+=1
        print("")
if __name__ == '__main__':
    main()
