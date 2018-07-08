# encoding: utf-8

import os

if __name__ == '__main__':
    fhandler = os.popen('top -bn 1')
    lines = fhandler.readlines()

    cpu = float(lines[2].split()[1])

    mem_total = lines[3].split()[3]
    mem_free = lines[3].split()[5]
    mem_use = lines[3].split()[7]
#    mem_buffers = int(lines[3].split(' ')[9])/1024

    mem = 100 * float(mem_use)/float(mem_total)
    fhandler.close()
    print(cpu)
    print(mem)