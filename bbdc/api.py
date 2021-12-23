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
class BBDC(object):
	"""docstring for BBDC"""
	# 单例模式加锁
	_instance_lock = threading.Lock()
	
	def __init__(self):
		env_list = ['BBDC_USERID']
		all_right, no_env = common.check_env(env_list)
		if not all_right:
			raise Exception("未设置必要环境变量 %s" % no_env)
		if not hasattr(self, 'userid'):
			self.userid = os.getenv("BBDC_USERID")
		if not hasattr(self, 'habit_name'):
			self.habit_name = LC().get_habit_name_by_project_name("不背单词")
		if not hasattr(self, 'habit_id'):
			self.habit_id = Habitica().get_habitica_habit_id_by_name(self.habit_name)

	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with BBDC._instance_lock:
				if not hasattr(cls, '_instance'):
					BBDC._instance = super().__new__(cls)
		return BBDC._instance
	# 获取最近7天背单词数
	def get_latest_learn_list(self):
		get_user_url = 'https://learnywhere.cn/bb/dashboard/profile/search?userId=%s' % self.userid
		user_res = requests.get(get_user_url)
		user_json = json.loads(user_res.text)
		if user_json['result_code'] == 200:
			return user_json['data_body']['learnList']
		else:
			raise Exception("获取单词数据出现异常 %s" % str(user_json))
	
	# 获取当天背单词数
	def get_today_learn_number(self):
		latest_learn_list = self.get_latest_learn_list()
		return latest_learn_list[-1]['learnNum']

	# 获取当天复习数量
	def get_today_review_number(self):
		latest_learn_list = self.get_latest_learn_list()
		return latest_learn_list[-1]['reviewNum']

	# 获取当天学习数据(包含 learnNum - 背单词数量 reviewNum - 复习数量)
	def get_today_words_data(self):
		latest_learn_list = self.get_latest_learn_list()
		return latest_learn_list[-1]
	
	# 获取当天背单词总数(背单词数量 + 复习数量)
	def get_today_total_words(self):
		today_words_data = self.get_today_words_data()
		return today_words_data['learnNum'] + today_words_data['reviewNum']
	
	# 获取在 leancloud 的最近的学习数据
	def get_latest_lc_data(self):
		now = common.get_china_now()
		query = leancloud.Query('BBDC')
		query.descending('date')
		try:
			latest_data = query.first()
		except LeanCloudError as e:
			if e.code == 101:
				return {
					'date' : now,
					'learnNum' : 0,
					'reviewNum' : 0,
					'total' : 0
				}
		data = {
			'date' : latest_data.get('date'),
			'learnNum' : latest_data.get('learnNum'),
			'reviewNum' : latest_data.get('reviewNum'),
			'total' : latest_data.get('total')
		}
		return data
	# 获取leancloud数据
	def get_lc_data(self, page):
		now = common.get_china_now()
		query = leancloud.Query('BBDC')
		query.descending('date')
		query.limit(20)
		query.skip(page * 20)
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
				'learnNum' : item.get('learnNum'),
				'reviewNum' : item.get('reviewNum'),
				'total' : item.get('total'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
				'oldTotal' : item.get('oldTotal'),
				'oldLearnNum' : item.get('oldLearnNum'),
				'oldReviewNum' : item.get('oldReviewNum'),
			}
			data_list.append(data)
		return data_list
	def set_lc_data(self, words_data, OldUser, NewUser, DiffUser):
		latest_lc_data = self.get_latest_lc_data()
		now = common.get_china_now()
		# 如果不是同一天
		if not common.is_same_day(latest_lc_data['date'], common.get_china_now()):
			latest_lc_data['total'] = latest_lc_data['learnNum'] = latest_lc_data['reviewNum'] = 0
		TodayBBDC = leancloud.Object.extend('BBDC')
		today_BBDC = TodayBBDC()
		today_BBDC.set('learnNum', words_data['learnNum'])
		today_BBDC.set('oldLearnNum', latest_lc_data['learnNum'])
		today_BBDC.set('reviewNum', words_data['reviewNum'])
		today_BBDC.set('oldReviewNum', latest_lc_data['reviewNum'])
		today_BBDC.set('total', words_data['reviewNum'] + words_data['learnNum'])
		today_BBDC.set('oldTotal', latest_lc_data['learnNum'] + latest_lc_data['reviewNum'])
		today_BBDC.set('oldUser', OldUser.toJSON())
		today_BBDC.set('newUser', NewUser.toJSON())
		today_BBDC.set('diffUser', DiffUser.toJSON())
		today_BBDC.set('info', DiffUser.get_diff_info())
		today_BBDC.set('date', now)
		today_BBDC.save()
	# 获取今日已背单词与今日已导入单词差异数量
	def get_today_lc_diff(self):
		latest_lc_data = self.get_latest_lc_data()
		today_total_words = self.get_today_total_words()
		diff = 0
		# 如果是同一天
		if common.is_same_day(latest_lc_data['date'], common.get_china_now()):
			diff = today_total_words - latest_lc_data['total']
		else:
			diff = today_total_words
		return diff
		# latest_lc_total_words
	# 获取需要进行完成 habit 的次数
	def get_do_habitica_habit_times(self):
		# 点一次习惯的步长
		word_steps = os.getenv("BBDC_STEPS")
		if not word_steps:
			word_steps = 20
		today_lc_diff = self.get_today_lc_diff()
		return int(today_lc_diff / int(word_steps))

	# 每日导出数据到habitica
	def habitica_daily_export(self):
		hc = Habitica()
		OldUser = hc.get_habitica_user()
		do_habitica_habit_times = self.get_do_habitica_habit_times()
		NewUser = copy.copy(OldUser)
		res = "你还没有背满应该背的单词哦! 快去背单词吧！"
		if do_habitica_habit_times != 0:
			for time in range(do_habitica_habit_times):
				NewUser = hc.do_habitica_habit_by_id(self.habit_id)
			DiffUser = NewUser - OldUser
			words_data = self.get_today_words_data()
			self.set_lc_data(words_data, OldUser, NewUser, DiffUser)
			common.send_push_plus("你的不背单词已导入 Habitica !", DiffUser.get_diff_info())
			res = DiffUser.get_diff_info()
		return res, do_habitica_habit_times