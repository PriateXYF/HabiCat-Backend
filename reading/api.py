import os
import requests
import json
import threading
import copy
import common
from habitica import Habitica
import leancloud
from leancloud import LeanCloudError
from lc.api import LC

# 提供不背单词基本操作
class Reading(object):
	"""docstring for Reading"""
	# 单例模式加锁
	_instance_lock = threading.Lock()
	
	def __init__(self):
		if not hasattr(self, 'habit_name'):
			self.habit_name = LC().get_habit_name_by_project_name("读书记录")
		if not hasattr(self, 'habit_id'):
			self.habit_id = Habitica().get_habitica_habit_id_by_name(self.habit_name)

	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with Reading._instance_lock:
				if not hasattr(cls, '_instance'):
					Reading._instance = super().__new__(cls)
		return Reading._instance
	
	# 获取在 leancloud 的最近的读书数据
	def get_latest_lc_data(self, book_name):
		now = common.get_china_now()
		query = leancloud.Query('Reading')
		if book_name:
			query.equal_to('bookName', book_name)
		query.descending('date')
		try:
			latest_data = query.first()
		except LeanCloudError as e:
			if e.code == 101:
				return {
					'date' : now,
					'bookName' : book_name,
					'bookPage' : 0,
				}
		data = {
			'date' : latest_data.get('date'),
			'bookName' : latest_data.get('bookName'),
			'bookPage' : latest_data.get('bookPage'),
		}
		return data
	# 获取leancloud数据
	def get_lc_data(self, page):
		now = common.get_china_now()
		query = leancloud.Query('Reading')
		query.descending('date')
		query.limit(10)
		query.skip(page * 10)
		lc_list = None
		try:
			lc_list = query.find()
		except LeanCloudError as e:
			if e.code == 101:
				return []
		data_list = []
		for item in lc_list:
			data = {
				'id' : item.id,
				'date' : item.get('date'),
				'bookName' : item.get('bookName'),
				'bookPage' : item.get('bookPage'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	def set_lc_data(self, book_data, OldUser, NewUser, DiffUser):
		now = common.get_china_now()
		TodayReading = leancloud.Object.extend('Reading')
		today_reading = TodayReading()
		today_reading.set('bookName', book_data['bookName'])
		today_reading.set('bookPage', book_data['bookPage'])
		today_reading.set('oldUser', OldUser.toJSON())
		today_reading.set('newUser', NewUser.toJSON())
		today_reading.set('diffUser', DiffUser.toJSON())
		today_reading.set('info', DiffUser.get_diff_info())
		today_reading.set('date', now)
		today_reading.save()

	# 每日导出数据到habitica
	def habitica_export(self, book_data):
		hc = Habitica()
		OldUser = hc.get_habitica_user()
		latest_lc_data = self.get_latest_lc_data(book_data['bookName'])
		do_habitica_habit_times = int(book_data['bookPage'] / 20) - int(latest_lc_data['bookPage'] / 20)
		NewUser = copy.copy(OldUser)
		res = "你还没有看满20页哦! 快去看书吧！"
		if do_habitica_habit_times != 0:
			for time in range(do_habitica_habit_times):
				NewUser = hc.do_habitica_habit_by_id(self.habit_id)
			DiffUser = NewUser - OldUser
			self.set_lc_data(book_data, OldUser, NewUser, DiffUser)
			common.send_push_plus("你的读书数据已导入 Habitica !", DiffUser.get_diff_info())
			res = DiffUser.get_diff_info()
		else if do_habitica_habit_times > 5:
			res = "你读太多书啦！一次不要超过 100 页哦！"
		else:
			DiffUser = NewUser - OldUser
			self.set_lc_data(book_data, OldUser, NewUser, DiffUser)
		return res, do_habitica_habit_times