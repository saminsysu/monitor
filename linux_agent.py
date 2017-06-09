#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
linux Agent
usage: 
	启动: python linux_agent.py start  
    关闭: python linux_agent.py stop  
    重启: python linux_agent.py restart
   	状态: python linux_agent.py status
'''

import os, sys

import monitor_client

def createDaemon():
	'''创建守护进程'''
	# try:
	# 	if os.fork() > 0:
	# 		os._exit(0)
	# except OSError, e:
	# 	print 'fork #1 failed: %d (%s)' % (e.errno, e.strerror)
	# 	os._exit(1)

	# os.chdir('/')
	# os.setsid()
	# os.umask(0)


	# try:
	# 	if os.fork() > 0:
	# 		os._exit(0)
	# except OSError, e:
	# 	print 'fork #2 failed: %d (%s)' % (e.errno, e.strerror)
	# 	os._exit(1)

	# #重定向标准输入流、标准输出流、标准错误
	# sys.stdout.flush()
	# sys.stderr.flush()
	# si = open(os.devnull, 'r')
	# so = open(os.devnull, 'a+')
	# se = open(os.devnull, 'a+', 0) #unbuffered
	# os.dup2(si.fileno(), sys.stdin.fileno())
	# os.dup2(so.fileno(), sys.stdout.fileno())
	# os.dup2(se.fileno(), sys.stderr.fileno())

	monitor_client.send_data()

if __name__ == '__main__':
	createDaemon()
