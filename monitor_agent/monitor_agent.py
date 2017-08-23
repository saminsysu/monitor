#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
收集监控数据，并定时发送到数据库InfluxDB中
'''
import os
import platform
import psutil
import time
import socket
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError

init_network_info = 0
interval = 15 #second

def get_host_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	while True:
	    try:
	        s.connect(('8.8.8.8', 80))
	        ip = s.getsockname()[0]
	    except:
	    	print("There is something wrong with network")
	    else:
	    	s.close()
	    	return ip

host_ip = get_host_ip()

def get_monitor_data():
	global init_network_info
	global interval
	monitor_data = []
	KB = 1024
	MB = 1024 * 1024
	GB = 1024 * 1024 * 1024	
	#####################################
	
	#system information
	sysInfo = platform.uname()
	sysname = sysInfo[0]
	# hostname = sysInfo[1]

	#获取CPU、网络、内存、硬盘等信息
	#network
	network = {'measurement':'network',
			'tags':{},
			'fields':{}
			}
	network_tags = network['tags']
	network_tags['host'] = host_ip
	network_info = psutil.net_io_counters()
	network_fields = network['fields']
	network_fields['bytes_sent'] = (network_info.bytes_sent - init_network_info.bytes_sent) / KB / interval #KB/s
	network_fields['bytes_rcvd'] = (network_info.bytes_recv - init_network_info.bytes_recv) / KB / interval #KB/s
	init_network_info = network_info
	monitor_data.append(network)

	#cpu
	#利用率
	cpu = {'measurement':'cpu',
			'tags':{},
			'fields':{}
			}
	cpu_tags = cpu['tags']
	cpu_tags['host'] = host_ip
	cpu_utilization = psutil.cpu_times_percent()
	cpu_fields = cpu['fields']
	cpu_fields['cpu_user'] = cpu_utilization.user
	cpu_fields['cpu_system'] = cpu_utilization.system
	cpu_fields['cpu_idle'] = cpu_utilization.idle
	cpu_fields['cpu_usage'] = psutil.cpu_percent()
	monitor_data.append(cpu)

	if sysname == 'Linux':
		#average load, 1min, 5min, 15min
		#Windows不存在平均负载
		load_1, load_5, load_15 = os.getloadavg()
		load = {'measurement':'load',
				'tags':{},
				'fields':{}
				}
		load_tags = load['tags']
		load_tags['host'] = host_ip
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
	disk_tags['host'] = host_ip
	disk_info = psutil.disk_usage('/')
	disk_fields = disk['fields']
	disk_fields['disk_total'] = disk_info.total / GB
	disk_fields['disk_used'] = disk_info.used / GB
	disk_fields['disk_free'] = disk_info.free / GB
	disk_fields['disk_usage'] = disk_info.percent
	monitor_data.append(disk)

	#memory
	memory = {'measurement':'memory',
			'tags':{},
			'fields':{}
			}
	memory_info = psutil.virtual_memory()
	memory_tags = memory['tags']
	memory_tags['host'] = host_ip
	memory_fields = memory['fields']
	memory_fields['memory_total'] = memory_info.total / MB
	memory_fields['memory_used'] = memory_info.used /MB
	memory_fields['memory_available'] = memory_info.available / MB
	memory_fields['memory_usage'] = memory_info.percent
	monitor_data.append(memory)

	#swap memory
	swap = {'measurement':'swap',
			'tags':{},
			'fields':{}
			}
	swap_info = psutil.swap_memory()
	swap_tags = swap['tags']
	swap_tags['host'] = host_ip
	swap_fields = swap['fields']
	swap_fields['swap_total'] = swap_info.total / MB
	swap_fields['swap_used'] = swap_info.used / MB
	swap_fields['swap_free'] = swap_info.free / MB

	monitor_data.append(swap)

	#########################################################
	#获取进程信息
	# if sysname == 'Linux':
	# 	for proc in psutil.process_iter():
	# 		process = {'measurement':'process',
	# 			'tags':{},
	# 			'fields':{}
	# 			}
	# 		process_tags = process['tags']
	# 		process_tags['host'] = host_ip
	# 		process_fields = process['fields']
	# 		try:
	# 			#speeds up the retrieval of multiple process information at the same time
	# 			with proc.oneshot():
	# 				process_tags['pid'] = proc.pid
	# 				process_fields['name'] = proc.name()
	# 				process_fields['username'] = proc.username()
	# 				# cpu使用率
	# 				process_fields['cpu_utilization'] = proc.cpu_percent()					
	# 		        # 内存使用率
	# 				process_fields['memory_utilization'] = proc.memory_percent()
	# 				if process_fields['cpu_utilization'] <= 0 and process_fields['memory_utilization'] <= 0:
	# 					continue
	# 		except psutil.NoSuchProcess:
	# 			pass
	# 		else:
	# 			monitor_data.append(process)
	return monitor_data

def send_monitor_data():
	global init_network_info
	global interval
	while True:
		try:
			client = InfluxDBClient(host='172.18.215.158', port=8086, database='server_stats')
		except:
			print("There is an error with connection to InfluxDB server!!!!")
		else:
			init_network_info = psutil.net_io_counters()
			time.sleep(interval)
			while True:
				monitor_data = get_monitor_data()
				try:
					client.write_points(monitor_data)
				except:
					print("There is an error with writing points to InfluxDB server!!!!")
				finally:
					time.sleep(interval)

if __name__ == '__main__':
	send_monitor_data()