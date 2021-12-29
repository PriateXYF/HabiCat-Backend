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
class Course(object):
	"""docstring for Course"""
	# 单例模式加锁
	_instance_lock = threading.Lock()
	
	def __init__(self):
		if not hasattr(self, 'habit_name'):
			self.habit_name = LC().get_habit_name_by_project_name("网课记录")
		if not hasattr(self, 'habit_id'):
			self.habit_id = Habitica().get_habitica_habit_id_by_name(self.habit_name)

	# 单例模式实现
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			with Course._instance_lock:
				if not hasattr(cls, '_instance'):
					Course._instance = super().__new__(cls)
		return Course._instance
	
	# 获取在 leancloud 的最近的读书数据
	def get_latest_lc_data(self, course_data):
		now = common.get_china_now()
		query = leancloud.Query('Course')
		query.equal_to('courseName', course_data['courseName'])
		query.equal_to('courseChapter', course_data['courseChapter'])
		query.descending('date')
		try:
			latest_data = query.first()
		except LeanCloudError as e:
			if e.code == 101:
				return {
					'date' : now,
					'courseName' : course_data['courseName'],
					'courseChapter' : course_data['courseChapter'],
					'courseSection' : 0,
				}
		data = {
			'date' : latest_data.get('date'),
			'courseName' : latest_data.get('courseName'),
			'courseChapter' : latest_data.get('courseChapter'),
			'courseSection' : latest_data.get('courseSection'),
		}
		return data
	# 获取leancloud数据
	def get_lc_data(self, page):
		now = common.get_china_now()
		query = leancloud.Query('Course')
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
				'Course' : item.get('Course'),
				'courseName' : item.get('courseName'),
				'courseChapter' : item.get('courseChapter'),
				'courseSection' : item.get('courseSection'),
				'oldUser' : item.get('oldUser'),
				'newUser' : item.get('newUser'),
				'diffUser' : item.get('diffUser'),
				'info' : item.get('info'),
			}
			data_list.append(data)
		return data_list
	def set_lc_data(self, course_data, OldUser, NewUser, DiffUser):
		now = common.get_china_now()
		TodayCourse = leancloud.Object.extend('Course')
		today_course = TodayCourse()
		today_course.set('courseName', course_data['courseName'])
		today_course.set('courseChapter', course_data['courseChapter'])
		today_course.set('courseSection', course_data['courseSection'])
		today_course.set('oldUser', OldUser.toJSON())
		today_course.set('newUser', NewUser.toJSON())
		today_course.set('diffUser', DiffUser.toJSON())
		today_course.set('info', DiffUser.get_diff_info())
		today_course.set('date', now)
		today_course.save()

	# 每日导出数据到habitica
	def habitica_export(self, course_data):
		hc = Habitica()
		OldUser = hc.get_habitica_user()
		latest_lc_data = self.get_latest_lc_data(course_data)
		do_habitica_habit_times = course_data['courseSection'] - latest_lc_data['courseSection']
		NewUser = copy.copy(OldUser)
		res = None
		if do_habitica_habit_times > 5:
			res = "你看太多课啦！一次不要超过5节！上次看到%d节了哦!" % latest_lc_data['courseSection']
		elif do_habitica_habit_times <= 0:
			res = "你是不是记错啦！上次已经看到%d节了哦！" % latest_lc_data['courseSection']
		else:
			for time in range(do_habitica_habit_times):
				NewUser = hc.do_habitica_habit_by_id(self.habit_id)
			DiffUser = NewUser - OldUser
			self.set_lc_data(course_data, OldUser, NewUser, DiffUser)
			common.send_push_plus("你的读书数据已导入 Habitica !", DiffUser.get_diff_info())
			res = DiffUser.get_diff_info()
		return res, do_habitica_habit_times