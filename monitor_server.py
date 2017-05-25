#-*-coding:utf-8-*-
# 多线程 监听端口 服务器
import socket
import threading
import json



def get_monitor_data(connection, address):
	monitor_data_str = connection.recv(2048)
	monitor_data = json.loads(monitor_data_str)
	# print(type(monitor_data_str))
	# print(monitor_data_str)
	# print(type(monitor_data))
	# print(monitor_data)
	connection.sendall(monitor_data_str)
	connection.close()


if __name__ == '__main__':
	ip_port = ("127.0.0.1", 5000)
	max_conn = 50
	server_socket = socket.socket()
	server_socket.bind(ip_port)
	server_socket.listen(max_conn)

	while True:
		conn, address = server_socket.accept()
		thread = threading.Thread(target=get_monitor_data, args=(conn, address))
		thread.start()