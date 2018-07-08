# encoding: utf-8

import os

if __name__ == '__main__':
	fhandler = os.popen('top -n 1')
	lines = fhandler.readlines()

	cpu = float(lines[2].split(' ')[2])

	mem_total = lines[3].split(' ')[4]
	mem_free = lines[3].split(' ')[8]
	mem_use = lines[3].split(' ')[12]
	mem_buffers = int(lines[3].split(' ')[15])/1024

	mem = 100 * float(mem_use)/float(mem_total)
	fhandler.close()
	print('cpu:',cpu,'%')
	print('mem:',int(mem),'%')