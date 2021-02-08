###################################
# Consumer 消费者
###################################
import time
from multiprocessing.managers import BaseManager

import CountingColors  # 引入采集助手包

import asyncio


def getImgUrl(url):
    '''获取图片的最终下载地址'''
    bf = CountingColors.getBf(url)
    url = bf.find(name="a", attrs={"class": "image_gall"})
    return url.get('href')


async def downImg(p, iq):  # 协程异步下载方法
    # def downImg(url):#常规下载方法
    '''下载每一个页面上的图片'''
    loop = asyncio.get_event_loop()

    imgurl = p.find(name="a").get("href")
    name = p.find(name="a").get("alt")
    data = [imgurl, name, ]
    data[0] = "https:" + await loop.run_in_executor(None, getImgUrl, "https:"+data[0])
    data.append(await loop.run_in_executor(None, CountingColors.getImgData, data[0]))
    # print(data[0], data[1])
    iq.put(data)
    print("{}已传输@@@@@@@@@@".format(data[1]))


def getImgUrls(l, iq):
    '''
    获取每个列表页上的所有图片最终的网页地址，并循环下载
    本函数式是本次下载的关键方法，是程序的核心。
    url: 图片列表页
    uq: 注册在网上的queue
    '''
    loop = asyncio.get_event_loop()
    bf = CountingColors.getBf(l)
    pageshtml = bf.find(name="div", attrs={"id": "container"})
    pageslist = pageshtml.find_all(name="p")
    # for p in pageslist:
    #     url = p.find(name="a").get("href")
    #     name= p.find(name="alt")
    #     data = [url,name,]
    # print(url)
    tasks = [downImg(p, iq) for p in pageslist]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))


# 注册一个管理器，负责管理调度网上注册的Queue队列
class ConsumerMagager(BaseManager):
    pass


def main():
    # 获取网络上的Queue 消费者，需要获取任务，计算后发送任务。
    ConsumerMagager.register('uq')
    ConsumerMagager.register('iq')
    m = ConsumerMagager(address=('192.168.0.88', 5678), authkey=b'2vv.net')
    m.connect()  # 连接服务器
    print("已连接到服务器")

    uq = m.uq()
    iq = m.iq()

    while True:
        if not uq.empty():  # 如果任务队列不为空
            l = uq.get(timeout=3)  # 如果超。
            getImgUrls(l, iq)

        else:
            time.sleep(1)
            print("好无聊，我在等待任务安排中")


if __name__ == '__main__':
    main()
