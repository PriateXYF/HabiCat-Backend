import leancloud
from common import get_china_now

# 在reading存储数据结束后修改Projects表
def after_course_save(_course):
	query = leancloud.Query('Projects')
	query.equal_to('name', '网课记录')
	project_course = query.first()
	project_course.set('latestUpdate', get_china_now())
	project_course.set('latestObject', _course.id)
	try:
		project_course.save()
	except leancloud.LeanCloudError:
		raise leancloud.LeanEngineError(message='An error occurred while trying to save the post.')