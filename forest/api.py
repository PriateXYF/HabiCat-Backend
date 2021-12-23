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
class Forest(object):
	"""docstring for Forest"""
	# 单例模式加锁
	_instance_lock = threading.Lock()
	def __init__(self):
		env_list = ['FOREST_SECRET', 'FOREST_AREA']
		all_right, no_env = common.check_env(env_list)
		if not all_right:
			raise Exception("未设置必要环境变量 %s" % no_env)
		if not hasattr(self, 'habit_name'):
			self.habit_name = LC().get_habit_name_by_project_name("Forest")
		if not hasattr(self, 'habit_id'):
			self.habit_id = Habitica().get_habitica_habit_id_by_name(self.habit_name)
		if not hasattr(self, 'secret'):
			self.secret = os.getenv("FOREST_SECRET")
		if not hasattr(self, 'area'):
			self.area = os.getenv("FOREST_AREA")
		if not hasattr(self, 'headers'):
			self.headers= {
				"cookie" : "remember_token={}".format(self.secret)
			}
	
	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with Forest._instance_lock:
				if not hasattr(cls, '_instance'):
					Forest._instance = super().__new__(cls)
		return Forest._instance

	# 读取 Forest 当天的数据并解析获取正式数据
	def read_forest_data(self, forest_json):
		res = []
		for item in forest_json:
			data = {
				'forestID' : item['id'],
				'date' : common.get_china_now(),
				'tag' : item['tag'],
				'note' : item['note'],
				'isSuccess' : item['is_success'],
				'startTime' : item['start_time'],
				'endTime' : item['end_time'],
				'treeCount' : item['tree_count'],
				'mode' : item['mode'],
				'trees' : item['trees']
			}
			res.append(data)
		return res

	# 获取 Forest 最近几天的数据(默认3天)
	def get_forest_data(self):
		now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=0))) - timedelta(days=3)
		# now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=0)))
		ts = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second).isoformat()
		# 国区
		url = "https://forest-china.upwardsware.com/api/v1/plants?seekrua=extension_chrome-5.0.8&from_date=%s" % ts 
		# 非国区
		if os.getenv("FOREST_AREA") != 'china':
			url = "https://c88fef96.forestapp.cc/api/v1/sessions?seekrua=extension_chrome-5.0.8&from_date=%s" % ts 
		forest_res = requests.get(url,headers=self.headers)
		forest_json = json.loads(forest_res.text)
		return forest_json
	
	# 获取在 leancloud 的最近三天的学习数据
	def get_latest_lc_data(self, days = 3):
		now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=0))) - timedelta(days=days)
		query = leancloud.Query('Forest')
		query.descending('date')
		query.greater_than_or_equal_to('date', now)
		lc_list = None
		try:
			lc_list = query.find()
		except LeanCloudError as e:
			if e.code == 101:
				return []
		data_list = []
		for item in lc_list:
			data = {
				'date' : item.get('date'),
				'id' : item.id,
				'forestID' : item.get('forestID'),
				'tag' : item.get('tag'),
				'note' : item.get('note'),
				'isSuccess' : item.get('isSuccess'),
				'startTime' : item.get('startTime'),
				'endTime' : item.get('endTime'),
				'treeCount' : item.get('treeCount'),
				'mode' : item.get('mode'),
				'trees' : item.get('trees'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	# 获取leancloud数据
	def get_lc_data(self, page = 0):
		query = leancloud.Query('Forest')
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
				'date' : item.get('date'),
				'id' : item.id,
				'forestID' : item.get('forestID'),
				'tag' : item.get('tag'),
				'note' : item.get('note'),
				'isSuccess' : item.get('isSuccess'),
				'startTime' : item.get('startTime'),
				'endTime' : item.get('endTime'),
				'treeCount' : item.get('treeCount'),
				'mode' : item.get('mode'),
				'trees' : item.get('trees'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	def set_lc_data(self, tree_data, OldUser, NewUser, DiffUser):
		now = common.get_china_now()
		TodayForest = leancloud.Object.extend('Forest')
		today_Forest = TodayForest()
		today_Forest.set('tag', tree_data['tag'])
		today_Forest.set('note', tree_data['note'])
		today_Forest.set('forestID', tree_data['forestID'])
		today_Forest.set('isSuccess', tree_data['isSuccess'])
		today_Forest.set('startTime', tree_data['startTime'])
		today_Forest.set('endTime', tree_data['endTime'])
		today_Forest.set('treeCount', tree_data['treeCount'])
		today_Forest.set('mode', tree_data['mode'])
		today_Forest.set('trees', tree_data['trees'])
		today_Forest.set('oldUser', OldUser.toJSON())
		today_Forest.set('newUser', NewUser.toJSON())
		today_Forest.set('diffUser', DiffUser.toJSON())
		today_Forest.set('info', DiffUser.get_diff_info())
		today_Forest.set('date', now)
		today_Forest.save()

	# 获取已完成habit与现有的差异
	def get_today_lc_diff(self):
		forest_data_list = self.get_forest_data()
		forest_data_list = self.read_forest_data(forest_data_list)
		latest_lc_data_list = self.get_latest_lc_data()
		res_list = []
		# print(forest_data)
		for forest_data in forest_data_list:
			flag = False
			for lc_data in latest_lc_data_list:
				# 如果lc中已有数据 或 种树失败 跳过
				if not forest_data['isSuccess'] or lc_data['forestID'] == forest_data['forestID']:
					flag = True
					break
			if flag:
				continue
			res_list.append(forest_data)
		return res_list
		# latest_lc_total_words

	# 每日导出数据到habitica
	def habitica_daily_export(self):
		today_diff_list = self.get_today_lc_diff()
		hc = Habitica()
		OldUser = hc.get_habitica_user()
		NewUser = copy.copy(OldUser)
		TrueOldUser = copy.copy(OldUser)
		res = "你还没有种好的新树哦! 快去种树吧！"
		if len(today_diff_list) != 0:
			for tree_data in today_diff_list:
				for temp in tree_data['trees']:
					NewUser = hc.do_habitica_habit_by_id(self.habit_id)
				DiffUser = NewUser - OldUser
				self.set_lc_data(tree_data, OldUser, NewUser, DiffUser)
				OldUser = NewUser
			DiffUser = NewUser - TrueOldUser
			common.send_push_plus("你的 Forest 已导入 Habitica !", DiffUser.get_diff_info())
			res = DiffUser.get_diff_info()
		return res, len(today_diff_list)