# encoding: utf-8

import os

if __name__ == '__main__':
    fhandler = os.popen('top')
    lines = fhandler.readlines()
    print(lines)
    fhandler.close()