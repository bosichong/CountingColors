###################################
# Producer 生产者
###################################
import random, time
from multiprocessing.managers import BaseManager

# 注册一个管理器，负责管理调度网上注册的Queue队列
class ProducerMagager(BaseManager):
    pass

def main():
    #获取网络上的Queue 消费者，需要获取任务，计算后发送任务。
    ProducerMagager.register('qq')
    ProducerMagager.register('uq')

    pm = ProducerMagager(address=('192.168.0.88',5678),authkey=b'2vv.net')
    pm.connect()#连接服务器
    print("已连接到服务器")

    task = pm.uq()#获取生产者的队列
    k = 1
    #
    while True:
        for i in range(10):
            r = random.randint(0,999)
            task.put(r)
        print("第{0}轮任务完毕！稍后继续！".format(k))
        k += 1
        time.sleep(3)

if __name__ == '__main__':
    main()


