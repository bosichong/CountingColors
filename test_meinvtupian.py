#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''

Chinaz美女图片采集
https://sc.chinaz.com/tupian/meinvtupian_2.html

采集排名前10页

'''

import CountingColors  # 引入采集助手包
from CountingColors import t


import re
import asyncio

###### Sun Jan 31 18:13:13 CST 2021


IMAGES_PATH = './chinaztu/'#存放图片的总目录
pool = CountingColors.createPool(10)




def getImgUrl(url):
    '''获取图片的最终下载地址'''
    bf = CountingColors.getBf(url)
    url = bf.find(name="a",attrs={"class":"image_gall"})
    return url.get('href')


async def downImg(url):#协程异步下载方法
# def downImg(url):#常规下载方法
    '''下载每一个页面上的图片'''
    loop = asyncio.get_event_loop()
    a = "https:{}".format(url.get("href"))
    # imgurl = "https:"+getImgUrl(a)# 常规获取图片链接地址
    imgurl =  "https:" + await loop.run_in_executor(None,getImgUrl,a)#asyncio获取图片链接地址
    # print(imgurl)
    imgname = re.search(r'[^/]+.jpg',imgurl).group()#图片名称
    imgpath = IMAGES_PATH+imgname
    # 单线程下载 序运行时间:41.49秒
    # CountingColors.saveImage(imgurl,imgpath) 
    # #多线程采集图片程序运行时间:18.90秒
    # pool.submit(CountingColors.saveImage,imgurl,imgpath)
    # asyncio 协程异步下载 程序运行时间:5.60秒
    await loop.run_in_executor(None,CountingColors.saveImage,imgurl,imgpath)
    print("{}保存成功".format(imgpath))

def getImgUrls(url):
    '''
    获取每个列表页上的所有图片最终的网页地址，并循环下载
    本函数式是本次下载的关键方法，是程序的核心。
    url: 图片列表页
    return list 一个列表页上所有图片的网页地址
    '''
    bf = CountingColors.getBf(url)#获取当前网页的bs4对象，用来解析HTML
    pageshtml = bf.find(name="div",attrs={"id":"container"})
    pageslist = pageshtml.find_all(name="a")

    # 常规的单线程 多线程保存图片 
    # for url in pageslist:
    #     downImg(url) #常规和多线程下载
    ####asyncio 异步下载图片
    tasks = [downImg(url) for url in pageslist ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


        


def getPageList(s=2,e=4):
    '''
    生成图片列表链接
    默认采集1-10页测试
    s:起始页
    e:结束页
    '''
    pages = ["https://sc.chinaz.com/tupian/meinvtupian.html",]#列表第一页
    #循环添加需要下载的列表页
    for i in range(s,e):
        pages.append("https://sc.chinaz.com/tupian/meinvtupian_"+str(i)+".html")
    return pages

@t
def main():

    CountingColors.createDir(IMAGES_PATH)#创建图片保存目录
    # 单个列表页上所有图片下载测试
    # getImgUrls("https://sc.chinaz.com/tupian/meinvtupian_2.html")
    
    
    #连续下载3页图片测试！
    for page in getPageList():
        getImgUrls(page)
        
    CountingColors.closePool(pool)
    


if __name__ == '__main__':
    main()
    