#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 09:17:39 2021

@author: J_sky
数彩
一个通用的采集助手包，封装了一些Request、BeautifulSoup、Re等在采集中经常使用的方法。
封装了一些多线程采集方法，及一些简单的分布式的采集方法。
"""

__version__ = "1.0.0"

__all__ = [

    "getHtmlCode", "getBf","saveImage","createDir","createPool","closePool",
    "t","getImgData"

]

import requests  # requests
from bs4 import BeautifulSoup  # html解析选择器

from . utils import *

import os
import time
import functools
import asyncio
from concurrent.futures import ThreadPoolExecutor#线程池



######### requests #########


def getHtmlCode(url):
    '''
    返回html代码
    :param url: 网页地址
    '''

    try:
        r = requests.get(url,
                         headers={
                             'User-Agent': get_user_agent_pc()
                         }
                         )
        r.raise_for_status()#判断网页是否正常采集，否则抛出错误
        r.encoding = r.apparent_encoding #分析编码并设置
        return r.text
    except:
        return "采集HTML代码失败,状态码：{}".format(r.status_code)


####### BeautifulSoup ######

def getBf(url):
    '''
    返回一个BeautifulSoup对象，用来处理HTML结构

    url : 网页地址


    '''
    return BeautifulSoup(getHtmlCode(url), 'html.parser')


if __name__ == '__main__':
    print(getBf("http://data.10jqka.com.cn/rank/lxsz/"))



###############IO相关操作#################


def createDir(path):
    '''
    若目录不存在则，创建一个目录
    :param path: 路径地址 请传入目录的绝对地址

    path = os.path.dirname(os.path.abspath(__file__))
    IMAGES_PATH = os.path.join(path,"chinaztu")

    '''
    if not os.path.exists(path):
        os.makedirs(path)


def getImgData(url):
    '''
    获得网络图片的字节流
    '''
    r = requests.get(url)
    return r.content

def saveImage(url,imgpath): 
    '''
    保存网络上的图片

    :param url : 图片的地址

    :param imgpath : 图片要保存的地址
    '''
    # urlretrieve(url, imgpath)  
    r = requests.get(url)
    with open(imgpath, 'wb') as f:
        f.write(r.content)     


def createPool(i):
    '''
    创建一个线程池

    :param i : 线程数
    '''
    print("创建了一个有{}条线程的线程池！".format(i))
    return ThreadPoolExecutor(10) #建立一个线程池

def closePool(pool):
    '''
    关闭线程池

    :param pool :线程池
    
    '''
    pool.shutdown()
    print("线程池已释放！")


def t(fun):
    '''

    定义一个程序运行时间计算函数
    
    '''
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        start = time.time()  # 起始时间
        fun(*args, **kwargs)  # 要执行的函数
        end = time.time()  # 结束时间
        print(fun.__name__, '程序运行时间:{:.2f}秒'.format((end - start)))
    return wrapper