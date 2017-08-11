#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
生成监控图
'''
import pygal
from influxdb import InfluxDBClient

def generate_image():
	'''
	根据监控数据生成监控图
	'''
	dateline = pygal.DateLine()
	

def get_monitor_stats(duration=30, metric=None, UUID=None, is_vm=False):
	'''
	根据节点、时间、指标参数从数据库中检索数据
	'''
	if is_vm:
		client = InfluxDBClient(host='127.0.0.1', port=8086, database='vm_stats')
	else:
		client = InfluxDBClient(host='127.0.0.1', port=8086, database='server_stats')

	rs = client.query("SELECT user_utilization from cpu where time >= now() - 1d")
	cpu_points = list(rs.get_points(measurement='cpu'))
	return cpu_points

get_monitor_stats()

