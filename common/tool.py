import os
import json
import requests
import leancloud
# from datetime import tzinfo, timedelta, datetime, timezone
import time
from datetime import datetime
import pytz as pytz

# 检测环境变量是否存在
def check_env(env_list):
	for env in env_list:
		if not os.getenv(env):
			return False, env
	return True, None

# 获取国区当前时间
def get_china_now():
	tz = pytz.timezone('Asia/Shanghai')
	now_time = datetime.fromtimestamp(int(time.time()), tz)
	return now_time

# 获取美区当前时间
def get_us_now():
	tz = timezone('US/Eastern')
	# now_time = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=0)))
	now_time = datetime.fromtimestamp(int(time.time()), tz)
	return now_time

# 判断两个datetime是否为同一天
def is_same_day(time1, time2):
	if time1.year != time2.year or time1.month != time2.month or time1.day != time2.day:
		return False
	return True

# 推送PUSH_PLUS消息
def send_push_plus(title, info):
	push_plus = os.getenv("PUSH_PLUS")
	if not push_plus or not info:
		return False, "未设置环境变量 PUSH_PLUS 或消息内容不存在"
	data = {
		"token" : push_plus,
		"title": title,
		"content" : info
	}
	body = json.dumps(data).encode(encoding='utf-8')
	headers = {'Content-Type':'application/json'}
	push_res = requests.post('http://www.pushplus.plus/send',data=body,headers=headers)
	push_json = json.loads(push_res.text)
	if push_json['code'] == 200:
		return True, push_json['msg']
	else:
		return False, push_json['msg']

# 获取全部lc项目
def get_lc_projects():
	query = leancloud.Query('Projects')
	lc_list = query.find()
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

def get_habit_name_by_project_name(project_name):
	query = leancloud.Query('Projects')
	query.equal_to('name', project_name)
	habit = query.first()
	return habit.get('habitName')
