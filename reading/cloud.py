import leancloud
from common import get_china_now

# 在reading存储数据结束后修改Projects表
def after_reading_save(_reading):
	query = leancloud.Query('Projects')
	query.equal_to('name', '读书记录')
	project_reading = query.first()
	project_reading.set('latestUpdate', get_china_now())
	project_reading.set('latestObject', _reading.id)
	try:
		project_reading.save()
	except leancloud.LeanCloudError:
		raise leancloud.LeanEngineError(message='An error occurred while trying to save the post.')