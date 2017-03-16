import threading
import time


class Num:
    def __init__(self):
        self.num = 0
        self.sem = threading.Semaphore(value=3)
        # 允许最多三个线程同时访问资源

    def add(self):
        self.sem.acquire()  # 内部计数器减1
        self.num += 1
        num = self.num
        self.sem.release()  # 内部计数器加1
        return num


n = Num()


class jdThread(threading.Thread):
    def __init__(self, item):
        threading.Thread.__init__(self)
        self.item = item

    def run(self):
        time.sleep(2)
        value = n.add()
        print(self.item, value)


for item in range(100):
    t = jdThread(item)
    t.start()
    t.join()