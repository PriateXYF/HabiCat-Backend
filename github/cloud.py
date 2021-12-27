from .api import GitHub
import leancloud
from common import get_china_now


def github_daily_habit(params):
	github = GitHub()
	return github.habitica_daily_export()

# 在GitHub存储数据结束后修改Projects表
def after_github_save(_github):
	query = leancloud.Query('Projects')
	query.equal_to('name', 'GitHub')
	project_github = query.first()
	project_github.set('latestUpdate', get_china_now())
	project_github.set('latestObject', _github.id)
	try:
		project_github.save()
	except leancloud.LeanCloudError:
		raise leancloud.LeanEngineError(message='An error occurred while trying to save the post.')