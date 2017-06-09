#!/usr/bin/env python
#-*-coding:utf-8-*-
'''客户端收集监控数据，并定时存储到数据库InfluxDB中'''
import socket
import psutil
import json
import time
import os
from influxdb import InfluxDBClient

def get_monitor_data():
	monitor_data = []
	#####################################
	#获取CPU、网络、内存、硬盘等信息
	#system information
	sysInfo = os.uname()
	sys_info = sysInfo[0] + ' ' +  sysInfo[2] + ' (' + sysInfo[4] + ')'
	#network
	network = {'measurement':'network',
			'tags':{},
			'fields':{}
			}
	network_tags = network['tags']
	network_tags['host'] = '172.18.215.158'
	pre_network_info = psutil.net_io_counters()
	interval = 2 #seconds
	time.sleep(interval)
	network_info = psutil.net_io_counters()
	network_fields = network['fields']
	network_fields['bytes_send_per_second'] = (network_info.bytes_sent - pre_network_info.bytes_sent) / interval #B/s
	network_fields['bytes_recv_per_second'] = (network_info.bytes_recv - pre_network_info.bytes_recv) / interval #B/s
	monitor_data.append(network)

	#cpu
	#利用率
	cpu = {'measurement':'cpu',
			'tags':{},
			'fields':{}
			}
	cpu_tags = cpu['tags']
	cpu_tags['host'] = '172.18.215.158'
	cpu_utilization = psutil.cpu_times_percent()
	cpu_fields = cpu['fields']
	cpu_fields['user_utilization'] = cpu_utilization.user
	cpu_fields['system_utilization'] = cpu_utilization.system
	cpu_fields['idle_utilization'] = cpu_utilization.idle
	#逻辑cpu数
	cpu_fields['cpu_count'] = psutil.cpu_count()
	monitor_data.append(cpu)

	#average load, 1min, 5min, 15min
	load_1, load_5, load_15 = os.getloadavg()
	load = {'measurement':'average_load',
			'tags':{},
			'fields':{}
			}
	load_tags = load['tags']
	load_tags['host'] = '172.18.215.158'
	load_fields = load['fields']
	load_fields['load_1'] = load_1
	load_fields['load_5'] = load_5
	load_fields['load_15'] = load_15
	monitor_data.append(load)

	#disk
	disk = {'measurement':'disk',
			'tags':{},
			'fields':{}
			}
	disk_tags = disk['tags']
	disk_tags['host'] = '172.18.215.158'
	disk_info = psutil.disk_usage('/')
	disk_fields = disk['fields']
	disk_fields['disk_total'] = disk_info.total
	disk_fields['disk_free'] = disk_info.free
	disk_fields['disk_utilization'] = disk_info.percent
	monitor_data.append(disk)
	
	#memory
	memory = {'measurement':'memory',
			'tags':{},
			'fields':{}
			}
	memory_info = psutil.virtual_memory()
	memory_tags = memory['tags']
	memory_tags['host'] = '172.18.215.158'
	memory_fields = memory['fields']
	memory_fields['memory_total'] = memory_info.total
	memory_fields['memory_used'] = memory_info.used
	memory_fields['memory_available'] = memory_info.available
	monitor_data.append(memory)

	#swap memory
	swap = {'measurement':'swap',
			'tags':{},
			'fields':{}
			}
	swap_info = psutil.swap_memory()
	swap_tags = swap['tags']
	swap_tags['host'] = '172.18.215.158'
	swap_fields = swap['fields']
	swap_fields['swap_total'] = swap_info.total
	swap_fields['swap_used'] = swap_info.used
	swap_fields['swap_free'] = swap_info.free

	monitor_data.append(swap)

	#########################################################
	#获取进程信息
	for proc in psutil.process_iter():
		process = {'measurement':'process',
			'tags':{},
			'fields':{}
			}
		process_tags = process['tags']
		process_tags['host'] = '172.18.215.158'
		process_fields = process['fields']
		try:
			#speeds up the retrieval of multiple process information at the same time		
			with proc.oneshot():
				process_tags['pid'] = proc.pid
				process_fields['name'] = proc.name()
				process_fields['username'] = proc.username()
				# cpu使用率,第一次为0
				process_fields['cpu_utilization'] = proc.cpu_percent()					
		        # 内存使用率
				process_fields['memory_utilization'] = proc.memory_percent()
			if process_fields['cpu_utilization'] > 0:
				print process_fields['cpu_utilization']
		except psutil.NoSuchProcess:
			pass
		else:
			monitor_data.append(process)
	return monitor_data

def send_data():
	client = InfluxDBClient(host='127.0.0.1', port=8086, database='monitor')
	interval = 15 #second
	while True:
		monitor_data = get_monitor_data()
		client.write_points(monitor_data)
		time.sleep(interval)

if __name__ == '__main__':
	send_data()
	