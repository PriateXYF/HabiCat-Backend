import os
import requests
import json
from common import check_env
import threading
import leancloud
from leancloud import LeanCloudError
from . import projects

class LC(object):
	_instance_lock = threading.Lock()
	"""docstring for Habitica"""
	def __init__(self):
		super(LC, self).__init__()
	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with LC._instance_lock:
				if not hasattr(cls, '_instance'):
					LC._instance = super().__new__(cls)
		return LC._instance
	def init_LC(self):
		self.init_projects()
		self.init_class('BBDC')
		self.init_class('Forest')
		self.init_class('Reading')
		self.init_class('GitHub')
		self.init_class('Course')
	def get_lc_projects(self):
		query = leancloud.Query('Projects')
		try:
			lc_list = query.find()
		except LeanCloudError as e:
			if e.code == 101:
				lc_list = []
			else:
				raise e
		data_list = []
		for item in lc_list:
			data = {
				'id' : item.id,
				'latestUpdate' : item.get('latestUpdate'),
				'isOpen' : item.get('isOpen'),
				'name' : item.get('name'),
				'path' : item.get('path'),
				'category' : item.get('category'),
				'isShow' : item.get('isShow'),
				'habitName' : item.get('habitName'),
				'password' : item.get('password'),
			}
			data_list.append(data)
		return data_list
	def get_habit_name_by_project_name(self, project_name):
		query = leancloud.Query('Projects')
		query.equal_to('name', project_name)
		habit = query.first()
		return habit.get('habitName')
	# 判断是否存在class
	def has_class(self, class_name):
		query = None
		result = True
		query = leancloud.Query(class_name)
		try:
			query.first()
		except LeanCloudError as e:
			if e.code == 101:
				result = False
		return result
	# 创建类
	def init_class(self, class_name):
		if not self.has_class(class_name):
			_Class = leancloud.Object.extend(class_name)
			_class = _Class()
			res = _class.save()
			query = _Class.query
			init = query.first()
			init.destroy()
			print("Class %s 初始化成功!" % class_name)
	# 创建项目
	def init_projects(self):
		if not self.has_class("Projects"):
			projects.init_BBDC_project()
			projects.init_forest_project()
			projects.init_github_project()
			projects.init_reading_project()
			projects.init_course_project()