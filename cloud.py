# coding: utf-8

from leancloud import Engine
# from leancloud import LeanEngineError
# from forest import cloud as ForestCloud
from bbdc import bbdc_daily_habit as BBDCCloud
from forest import forest_daily_habit as ForestCloud
from github import github_daily_habit as GitHubCloud
from bbdc import after_BBDC_save as BBDCAfter
from forest import after_forest_save as ForestAfter
from github import after_github_save as GitHubAfter

engine = Engine()

# 不背单词每日导入
@engine.define
def bbdc_daily_habit(**params):
	return BBDCCloud(params)

# Forest每日导入
@engine.define
def forest_daily_habit(**params):
	return ForestCloud(params)

# GitHub每日导入
@engine.define
def github_daily_habit(**params):
	return GitHubCloud(params)

# 不背单词 hook
@engine.after_save('BBDC')
def after_BBDC(_bbdc):
	return BBDCAfter(_bbdc)

# Forest hook
@engine.after_save('Forest')
def after_forest(_forest):
	return ForestAfter(_forest)

# GitHub hook
@engine.after_save('GitHub')
def after_github(_github):
	return GitHubAfter(_github)