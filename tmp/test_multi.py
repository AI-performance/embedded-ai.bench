#!/usr/bin/env python
# ref:https://www.cnblogs.com/freeaihub/p/13401920.html
import threading
from time import ctime, sleep


# 对MyThread进行封装
class MyThread(threading.Thread):
    def __init__(self, func, args, name=""):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name
        self.args = args

    def run(self):
        print("开始执行", self.name, " 在：", ctime())
        self.res = self.func(*self.args)
        print(self.name, "结束于：", ctime())

    def getResult(self):
        return self.res


# 斐波那契
def fib(x):
    sleep(0.005)
    if x < 2:
        return 1
    return fib(x - 1) + fib(x - 2)


# 阶乘
def fac(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x * fac(x - 1)


# 累加
def sum(x):
    sleep(0.1)
    if x < 2:
        return 1
    return x + sum(x - 1)


funcs = [fib, fac, sum]
n = 12


def main():
    nfuncs = range(len(funcs))

    # 单线程
    print("单线程模式")
    for i in nfuncs:
        print("开始", funcs[i].__name__, " 在：", ctime())
        print(funcs[i](n))
        print(funcs[i].__name__, "结束于：", ctime())

    # 多线程
    print("多线程模式")
    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (n,), funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()
        print(threads[i].getResult())

    print("所有的任务结束")


main()
