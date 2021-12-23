import os
import requests
import json
from common import check_env
import threading

class HabiticaUser():
	def __init__(self, userdata):
		self.gp = userdata['gp']
		self.lvl = userdata['lvl']
		self.exp = userdata['exp']
	def __str__(self):
		return '{ "lvl" : "%d" , "exp" : "%.2f" , "gp" : "%.2f" }' % (self.lvl, self.exp, self.gp)
	def __add__(self, other):
		user = {
			'gp' : self.gp + other.gp,
			'lvl' : self.lvl + other.lvl,
			'exp' : self.exp + other.exp
		}
		return HabiticaUser(user)
	def __sub__(self, other):
		user = {
			'gp' : self.gp - other.gp,
			'lvl' : self.lvl - other.lvl,
			'exp' : self.exp - other.exp
		}
		return HabiticaUser(user)
	# 对比两个用户的差异，并获取差异信息
	def get_diff_info(self):
		info = ""
		if self.lvl > 0:
			info += "你升了 %d 级 !" % self.lvl
		else:
			info += "你的经验值增加了: %.1f ! " % self.exp
		info += "并获得了 %.1f 金币 !" % self.gp
		return info
	def toJSON(self):
		return json.loads(str(self))

class Habitica(object):
	_instance_lock = threading.Lock()
	"""docstring for Habitica"""
	def __init__(self):
		env_list = ['HABITICA_USERID', 'HABITICA_SECRET']
		if not check_env(env_list):
			raise Exception("未设置必要环境变量!")
		super(Habitica, self).__init__()
		if not hasattr(self, 'userid'):
			self.userid = os.getenv("HABITICA_USERID")
		if not hasattr(self, 'secret'):
			self.secret = os.getenv("HABITICA_SECRET")
		if not hasattr(self, 'headers'):
			self.headers = {
				'x-client' : '4e34a688-a0d8-4623-aef8-aa304b3096b1',
				'x-api-user' : self.userid,
				'x-api-key' : self.secret
			}
	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with Habitica._instance_lock:
				if not hasattr(cls, '_instance'):
					Habitica._instance = super().__new__(cls)
		return Habitica._instance

	# 获取用户基本信息
	def get_habitica_user(self):
		get_user_url = 'https://habitica.com/api/v3/user'
		user_res = requests.get(get_user_url,headers=self.headers)
		user_json = json.loads(user_res.text)
		user = {}
		user['lvl'] = user_json['data']['stats']['lvl']
		user['gp'] = user_json['data']['stats']['gp']
		user['exp'] = user_json['data']['stats']['exp']
		return HabiticaUser(user)
	# 通过名字获取 habit_id
	def get_habitica_habit_id_by_name(self, habit_name):
		get_tasks_url = 'https://habitica.com/api/v3/tasks/user'
		# 进行查找获取 habit_id
		all_tasks_res = requests.get(get_tasks_url, headers=self.headers)
		all_tasks_json = json.loads(all_tasks_res.text)
		habit_id = None
		if not all_tasks_json['success'] :
			raise Exception(all_tasks_json['message'])
		for task in all_tasks_json['data']:
			if habit_name == task['text']:
				habit_id = task['id']
				break
		if not habit_id:
			raise Exception('习惯 : %s 不存在 !' % habit_name)
		return habit_id
	# 通过 habit_id 完成 habit
	def do_habitica_habit_by_id(self, habit_id):
		score_task_url = 'https://habitica.com/api/v3/tasks/%s/score/up' % habit_id
		info_list = []
		score_res = requests.post(score_task_url,headers=self.headers)
		score_json = json.loads(score_res.text)
		user = {}
		if score_json['success']:
			user['lvl'] = score_json['data']['lvl']
			user['gp'] = score_json['data']['gp']
			user['exp'] = score_json['data']['exp']
		else:
			raise Exception(score_json['message'])
		return HabiticaUser(user)
	
	# 通过 habit_name 完成 habit
	def do_habitica_habit_by_name(self, habit_name):
		habit_id = self.get_habitica_habit_id_by_name(habit_name)
		return self.do_habitica_habit_by_id(habit_id)