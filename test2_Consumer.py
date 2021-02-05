###################################
# Consumer 消费者
###################################
import time
from multiprocessing.managers import BaseManager

# 注册一个管理器，负责管理调度网上注册的Queue队列
class ConsumerMagager(BaseManager):
    pass

def main():
    #获取网络上的Queue 消费者，需要获取任务，计算后发送任务。
    ConsumerMagager.register('qq')
    ConsumerMagager.register('uq')
    ConsumerMagager.register('iq')

    m = ConsumerMagager(address=('192.168.0.88',5678),authkey=b'2vv.net')
    m.connect()#连接服务器
    print("已连接到服务器")
    
    uq = m.uq()
    iq = m.iq()

    #开始计算任务
    while True:
        if not uq.empty():#如果任务队列不为空
            n = uq.get(timeout=3)#如果超。
            print('收到计算任务{0}*{1}={2}'.format(n,n,n*n))
            iq.put('%d * %d = %d' %(n,n,n*n))
        else:
            time.sleep(1)
            print("好无聊，我在等待任务安排中")

if __name__ == '__main__':
    main()