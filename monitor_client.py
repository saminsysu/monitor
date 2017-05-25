#-*-coding:utf-8-*-
#客户端收集监控数据，并定时发送给服务器
import socket
import psutil
import json

def monitor_data():
	monitor_data = {}
	#cpu
	
	#disk
	disk_data = psutil.disk_usage('/')
	monitor_data['disk_data'] = disk_data
	
	#memory
	#network
	monitor_data_str = json.dumps(monitor_data)
	return monitor_data_str

if __name__ == '__main__':
	client_socket = socket.socket()
	client_socket.connect(("127.0.0.1", 5000))
	client_socket.sendall(monitor_data())
	ret = str(client_socket.recv(2048))
	print(ret)