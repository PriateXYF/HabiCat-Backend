import os
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

# 提供不背单词基本操作
class GitHub(object):
	"""docstring for GitHub"""
	# 单例模式加锁
	_instance_lock = threading.Lock()
	def __init__(self):
		env_list = ['GITHUB_USERNAME', 'GITHUB_SECRET']
		all_right, no_env = common.check_env(env_list)
		if not all_right:
			raise Exception("未设置必要环境变量 %s" % no_env)
		if not hasattr(self, 'habit_name'):
			self.habit_name = LC().get_habit_name_by_project_name("GitHub")
		if not hasattr(self, 'habit_id'):
			self.habit_id = Habitica().get_habitica_habit_id_by_name(self.habit_name)
		if not hasattr(self, 'secret'):
			self.secret = os.getenv("GITHUB_SECRET")
		if not hasattr(self, 'username'):
			self.username = os.getenv("GITHUB_USERNAME")
		if not hasattr(self, 'headers'):
			self.headers= {
				"Accept" : "application/vnd.github.v3+json"
			}

	
	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with GitHub._instance_lock:
				if not hasattr(cls, '_instance'):
					GitHub._instance = super().__new__(cls)
		return GitHub._instance

	# 读取 GitHub 当天的数据并解析获取正式数据
	def read_github_data(self, github_json):
		res = []
		for item in github_json:
			if item['type'] != 'PushEvent':
				continue
			data = {
				'pushId' : item['payload']['push_id'],
				'date' : common.get_china_now(),
				'repo' : item['repo']['name'],
				'size' : item['payload']['size'],
				'commits' : item['payload']['commits'],
			}
			res.append(data)
		return res

	# 获取 GitHub 最近的数据(默认30条)
	def get_github_data(self):
		url = "https://api.github.com/users/PriateXYF/events"
		github_res = requests.get(url, auth=(self.username, self.secret), headers=self.headers)
		github_json = json.loads(github_res.text)
		return github_json
	
	# 获取在 leancloud 的最近50条 GitHub 数据
	def get_latest_lc_data(self, limit = 50):
		# now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=0))) - timedelta(days=days)
		query = leancloud.Query('GitHub')
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
				'pushId' : item.get('pushId'),
				'date' : item.get('data'),
				'repo' : item.get('repo'),
				'size' : item.get('size'),
				'commits' : item.get('commits'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	# 获取leancloud数据
	def get_lc_data(self, page = 0):
		query = leancloud.Query('GitHub')
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
				'pushId' : item.get('pushId'),
				'date' : item.get('date'),
				'repo' : item.get('repo'),
				'size' : item.get('size'),
				'commits' : item.get('commits'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	
	def set_lc_data(self, github_data, OldUser, NewUser, DiffUser):
		now = common.get_china_now()
		TodayGitHub = leancloud.Object.extend('GitHub')
		today_github = TodayGitHub()
		today_github.set('pushId', github_data['pushId'])
		today_github.set('repo', github_data['repo'])
		today_github.set('size', github_data['size'])
		today_github.set('commits', github_data['commits'])
		today_github.set('oldUser', OldUser.toJSON())
		today_github.set('newUser', NewUser.toJSON())
		today_github.set('diffUser', DiffUser.toJSON())
		today_github.set('info', DiffUser.get_diff_info())
		today_github.set('date', now)
		today_github.save()

	# 获取已完成habit与现有的差异
	def get_today_lc_diff(self):
		github_data_list = self.get_github_data()
		github_data_list = self.read_github_data(github_data_list)
		latest_lc_data_list = self.get_latest_lc_data()
		res_list = []
		# print(GitHub_data)
		for github_data in github_data_list:
			flag = False
			for lc_data in latest_lc_data_list:
				# 如果 lc 中已有数据 跳过
				if lc_data['pushId'] == github_data['pushId']:
					flag = True
					break
			if flag:
				continue
			res_list.append(github_data)
		return res_list

	# 每日导出数据到habitica
	def habitica_daily_export(self):
		today_diff_list = self.get_today_lc_diff()
		hc = Habitica()
		OldUser = hc.get_habitica_user()
		NewUser = copy.copy(OldUser)
		TrueOldUser = copy.copy(OldUser)
		res = "你还没有新的GiHub提交哦 ! Coding Now!"
		if len(today_diff_list) != 0:
			for github_data in today_diff_list:
				for temp in github_data['commits']:
					NewUser = hc.do_habitica_habit_by_id(self.habit_id)
				DiffUser = NewUser - OldUser
				self.set_lc_data(github_data, OldUser, NewUser, DiffUser)
				OldUser = NewUser
			DiffUser = NewUser - TrueOldUser
			common.send_push_plus("你的 GitHub 已导入 Habitica !", DiffUser.get_diff_info())
			res = DiffUser.get_diff_info()
		return res, len(today_diff_list)