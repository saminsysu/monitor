#-*-coding:utf-8-*-
#客户端收集监控数据，并定时发送给服务器
import socket
import psutil
import json
import time
from influxdb import InfluxDBClient

def monitor_data():
	monitor_data = []
	#####################################
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

	#####################################
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
	#network
	# monitor_data_str = json.dumps(monitor_data)
	return monitor_data


if __name__ == '__main__':
	# client_ip_port = ("127.0.0.1", 8647)
	# server_ip_port = ("127.0.0.1", 5000)
	# while True:
	# 	#短连接。每一次发送数据都需要建立连接，发送完后断开连接
	# 	#可以考虑使用长连接
	# 	client_socket = socket.socket()
	# 	client_socket.bind(client_ip_port)
	# 	client_socket.connect(server_ip_port)
	# 	client_socket.sendall(monitor_data())
	# 	# print(monitor_data())
	# 	ret = str(client_socket.recv(2048))
	# 	print(ret)
	# 	client_socket.close()
	# 	time.sleep(15)
	#将数据存储在数据库influxdb中
	client = InfluxDBClient(host='127.0.0.1', port=8086, database='testDB')
	monitor_data = monitor_data()
	print monitor_data
	client.write_points(monitor_data)


