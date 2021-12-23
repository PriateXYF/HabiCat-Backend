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
	cst = pytz.timezone('Asia/Shanghai')  # 东八区
	t = datetime.fromtimestamp(int(time.time()), cst)
	return t

# 获取美区当前时间
def get_us_now():
	utc = pytz.timezone('UTC')
	t = datetime.fromtimestamp(int(time.time()), utc)
	return t

# 判断两个datetime是否为同一天
def is_same_day(time1, time2):
	cst = pytz.timezone('Asia/Shanghai')
	time1 = time1.astimezone(cst)
	time2 = time2.astimezone(cst)
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