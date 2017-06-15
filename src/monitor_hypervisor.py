#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
通过libvirt接口从KVM获得虚拟机信息
'''
import libvirt
import sys

def get_conn():
	'''
	获取libvirt的连接句柄，用于提供操作libivrt的接口
	'''
	try:
		conn = libvirt.open('qemu:///system')
	except Exception as e:
		print(e)
	else:
		if conn == None:
			print('Failed to open connection to qemu:///system')
			exit(1)
		else:
			return conn

def get_domains_data():
	'''
	通过调用libvirt接口获取虚拟机CPU、Disk、Memory、I/O数据
	'''
	monitor_data = []
	conn = get_conn()
	domIDs = conn.listDomainsID()
	if domIDs == None:
		print('Failed to get a list of domain IDs')
	else:
		for domID in domIDs:
			dom = conn.lookupByID(domID)
			if dom == None:
				print('Failed to find the domain '+domID)
			else:
				state, maxmem, mem, cpus, cput = dom.info()
				print(dom.isActive())
				print(dom.info())
				# print(dom.getCPUStats(0))
				# print(dom.memoryStats())

get_domains_data()

