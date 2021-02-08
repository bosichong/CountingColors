###################################
# Manager 源码
###################################
'''
Manager 主要负责创建程序需要的通信队列queue，负责保存调度任务，保存图片数据
程序中只有一个Manager。
'''
import time
import re
import queue
import os

import CountingColors

from multiprocessing.managers import BaseManager  # 分布式进程模块
from multiprocessing import freeze_support

path = os.path.dirname(os.path.abspath(__file__))
IMAGES_PATH = os.path.join(path,"chinaztu/")

# 创建两个queue 分别用来：通信（控制程序），url传递,图片数据传递
url_queue = queue.Queue()  # 图片列表URL的q
img_queue = queue.Queue()  # 发送图片URL的Q


def return_url_queue():
    return url_queue


def return_img_queue():
    return img_queue

# 注册一个管理器，负责管理调度网上注册的Queue队列
class GodManager(BaseManager):
    pass


def do_taskmaster():

    # 把任务队列通过管理器注册到网上，这样就可以在多台机器间访问通信，做到分布式通信。
    GodManager.register('uq', callable=return_url_queue)
    GodManager.register('iq', callable=return_img_queue)

    # 设置服务器的ip、端口及密码
    manager = GodManager(address=('192.168.0.88', 5678), authkey=b'2vv.net')
    manager.start()  # 启动服务器
    print('服务器已经启动！')
    # 重新获取已经在网上注册的队列,使用队列名()方法来获得网上注册的队列名。
    uq = manager.uq()
    iq = manager.iq()

    # 开始任务，无非就是三个任务：
    while True:
        if not uq.empty():  # 如果有消息发来
            time.sleep(1)
            print("还有好多任务没有完成！")
        elif not iq.empty():  # 如果发来图片，我来保存
            data = iq.get(timeout=3)
            imgname = data[1]+re.search(r'[^/]+.jpg', data[0]).group()  # 图片名称
            imgpath = IMAGES_PATH+imgname

            # 保存图片到硬盘
            with open(imgpath, 'wb') as f:
                f.write(data[2])
            print("{}已经保存到{}".format(data[1],imgpath))
        else:
            time.sleep(1)
            print("无聊的等待，他们干活的效率可真慢啊！")


if __name__ == '__main__':   # windows运行下,当这个文件被导入时候，如果用了这个if就可以避免没被封装的语句被执行
    CountingColors.createDir(IMAGES_PATH)#创建图片保存目录
    print("图片存储目录已创建！")
    freeze_support()
    print('To start putting tasks in the Queue...')
    do_taskmaster()
