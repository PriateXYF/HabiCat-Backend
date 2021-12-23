from .api import Forest
import leancloud
from common import get_china_now


def forest_daily_habit(params):
	forest = Forest()
	return forest.habitica_daily_export()

# 在Forest存储数据结束后修改Projects表
def after_forest_save(_forest):
	query = leancloud.Query('Projects')
	query.equal_to('name', 'Forest')
	project_Forest = query.first()
	project_Forest.set('latestUpdate', get_china_now())
	project_Forest.set('latestObject', _forest.id)
	try:
		project_Forest.save()
	except leancloud.LeanCloudError:
		raise leancloud.LeanEngineError(message='An error occurred while trying to save the post.')