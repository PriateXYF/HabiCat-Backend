import os
import feedparser
import requests
import json
import threading
import copy
import common
from habitica import Habitica
from datetime import datetime, timezone, timedelta
import leancloud
from leancloud import LeanCloudError
from lc.api import LC
from time import mktime
import pytz as pytz

# 提供不背单词基本操作
class Douban(object):
	"""docstring for GitHub"""
	# 单例模式加锁
	_instance_lock = threading.Lock()
	def __init__(self):
		env_list = ['DOUBAN_ID']
		all_right, no_env = common.check_env(env_list)
		if not all_right:
			raise Exception("未设置必要环境变量 %s" % no_env)
		if not hasattr(self, 'habit_name'):
			self.habit_name = LC().get_habit_name_by_project_name("豆瓣")
		if not hasattr(self, 'habit_id'):
			self.habit_id = Habitica().get_habitica_habit_id_by_name(self.habit_name)
		if not hasattr(self, 'user_id'):
			self.user_id = os.getenv("DOUBAN_ID")

	
	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with Douban._instance_lock:
				if not hasattr(cls, '_instance'):
					Douban._instance = super().__new__(cls)
		return Douban._instance

	# 读取 Douban 当天的数据并解析获取正式数据
	def read_douban_data(self, douban_list):
		res = []
		cst = pytz.timezone('GMT')
		for item in douban_list:
			data = {
				'interestId' : item['id'],
				'title' : item['title'],
				'link' : item['link'],
				'summary' : item['summary'],
				'date' : datetime.fromtimestamp(mktime(item['published_parsed']), cst),
			}
			res.append(data)
		return res

	# 通过 RSS 获取 Douban 最近的数据
	def get_douban_data(self):
		NewsFeed = feedparser.parse(f"https://www.douban.com/feed/people/{self.user_id}/interests")
		return NewsFeed.entries
	
	# 获取在 leancloud 的最近50条 Douban 数据
	def get_latest_lc_data(self, limit = 50):
		# now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=0))) - timedelta(days=days)
		query = leancloud.Query('Douban')
		query.descending('date')
		# query.greater_than_or_equal_to('date', now)
		query.limit(limit)
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
				'interestId' : item.get('interestId'),
				'title' : item.get('title'),
				'date' : item.get('date'),
				'link' : item.get('link'),
				'summary' : item.get('summary'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	# 获取leancloud数据
	def get_lc_data(self, page = 0):
		query = leancloud.Query('Douban')
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
				'interestId' : item.get('interestId'),
				'title' : item.get('title'),
				'date' : item.get('date'),
				'link' : item.get('link'),
				'summary' : item.get('summary'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	
	def set_lc_data(self, douban_data, OldUser, NewUser, DiffUser):
		TodayDouban = leancloud.Object.extend('Douban')
		today_douban = TodayDouban()
		today_douban.set('interestId', douban_data['interestId'])
		today_douban.set('title', douban_data['title'])
		today_douban.set('link', douban_data['link'])
		today_douban.set('summary', douban_data['summary'])
		today_douban.set('date', douban_data['date'])
		today_douban.set('oldUser', OldUser.toJSON())
		today_douban.set('newUser', NewUser.toJSON())
		today_douban.set('diffUser', DiffUser.toJSON())
		today_douban.set('info', DiffUser.get_diff_info())
		today_douban.save()

	# 获取已完成habit与现有的差异
	def get_today_lc_diff(self):
		douban_data_list = self.get_douban_data()
		douban_data_list = self.read_douban_data(douban_data_list)
		latest_lc_data_list = self.get_latest_lc_data()
		res_list = []
		# print(GitHub_data)
		for douban_data in douban_data_list:
			flag = False
			for lc_data in latest_lc_data_list:
				# 如果 lc 中已有数据 跳过
				if lc_data['interestId'] == douban_data['interestId']:
					flag = True
					break
			if flag:
				continue
			res_list.append(douban_data)
		return res_list

	# 每日导出数据到habitica
	def habitica_daily_export(self):
		today_diff_list = self.get_today_lc_diff()
		hc = Habitica()
		OldUser = hc.get_habitica_user()
		NewUser = copy.copy(OldUser)
		TrueOldUser = copy.copy(OldUser)
		res = "你还没有新的豆瓣记录哦!"
		if len(today_diff_list) != 0:
			for douban_data in today_diff_list:
				NewUser = hc.do_habitica_habit_by_id(self.habit_id)
				DiffUser = NewUser - OldUser
				self.set_lc_data(douban_data, OldUser, NewUser, DiffUser)
				OldUser = NewUser
			DiffUser = NewUser - TrueOldUser
			common.send_push_plus("你的豆瓣数据已导入 Habitica !", DiffUser.get_diff_info())
			res = DiffUser.get_diff_info()
		return res, len(today_diff_list)