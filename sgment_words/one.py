# -*- coding: utf-8 -*-

import threading

'''
多线程生成日志工具
'''


# 该方法主要用于写入300行WARN日志
def writeWarnLog(file):
    count = 0;
    while count < 300:
        try:
            file.write('2012-11-28 22:51:01|zookeeper|WARN|m1|172.17.1.15\n')
            count += 1
        except Exception as e:
            print('write warn log error', str(e))
            break
    print('write warn log finished')


# 该方法主要用于写入100行ERROR日志
def writeErrorLog(file):
    id = threading.currentThread().getName()
    count = 0
    while count < 100:
        try:
            file.write('2012-12-12 22:22:22|zookeeper|ERROR|m1|all\n')
            count += 1
        except Exception as e:
            print('write error log error', str(e))
            break
    print('write error log finished')


def main():
    fileName = 'zookeeper.log'
    mode = 'w+'  # 通过追加写日志文件
    # 创建两个线程来写文件
    try:
        f = open(fileName, mode)
        for i in range(5):
            t1 = threading.Thread(target=writeWarnLog, args=[f])
            t2 = threading.Thread(target=writeErrorLog, args=[f])

            t1.start()
            t2.start()
    except Exception as e:
        print('write log failed,', str(e))
    finally:
        f.close()
    print('write log finished')


if __name__ == '__main__':
    main()
