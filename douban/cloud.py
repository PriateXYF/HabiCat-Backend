from .api import Douban
import leancloud
from common import get_china_now


def douban_daily_habit(params):
	douban = Douban()
	return douban.habitica_daily_export()

# 在douban存储数据结束后修改Projects表
def after_douban_save(_douban):
	query = leancloud.Query('Projects')
	query.equal_to('name', '豆瓣')
	project_douban = query.first()
	project_douban.set('latestUpdate', get_china_now())
	project_douban.set('latestObject', _douban.id)
	try:
		project_douban.save()
	except leancloud.LeanCloudError:
		raise leancloud.LeanEngineError(message='An error occurred while trying to save the post.')