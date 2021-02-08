###################################
# Producer 生产者
###################################

import CountingColors  # 引入采集助手包
from CountingColors import t


import re
import time

from multiprocessing.managers import BaseManager


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


# 注册一个管理器，负责管理调度网上注册的Queue队列
class ProducerMagager(BaseManager):
    pass

def main():
    #获取网络上的Queue 消费者，需要获取任务，计算后发送任务。
    ProducerMagager.register('uq')
    pm = ProducerMagager(address=('192.168.0.88',5678),authkey=b'2vv.net')
    pm.connect()#连接服务器
    print("已连接到服务器")

    task = pm.uq()#获取生产者的队列
    
    pages = getPageList()

    for l in pages:
        task.put(l)
        # print(task.qsize())

    print("解析图片地址任务完成")

if __name__ == '__main__':
    main()


