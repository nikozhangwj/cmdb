# encoding: utf-8

import psutil

if __name__ == '__main__':
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    print(cpu)
    print(mem)