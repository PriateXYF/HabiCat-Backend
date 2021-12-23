from .api import BBDC
import leancloud
from common import get_china_now


def bbdc_daily_habit(params):
	bbdc = BBDC()
	return bbdc.habitica_daily_export()

# 在BBDC存储数据结束后修改Projects表
def after_BBDC_save(_bbdc):
	query = leancloud.Query('Projects')
	query.equal_to('name', '不背单词')
	project_BBDC = query.first()
	project_BBDC.set('latestUpdate', get_china_now())
	project_BBDC.set('latestObject', _bbdc.id)
	try:
		project_BBDC.save()
	except leancloud.LeanCloudError:
		raise leancloud.LeanEngineError(message='An error occurred while trying to save the post.')