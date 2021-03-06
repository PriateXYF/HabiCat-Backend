# coding: utf-8

from leancloud import Engine
# from leancloud import LeanEngineError
# from forest import cloud as ForestCloud
from bbdc import bbdc_daily_habit as BBDCCloud
from forest import forest_daily_habit as ForestCloud
from github import github_daily_habit as GitHubCloud
from douban import douban_daily_habit as DoubanCloud
from bbdc import after_BBDC_save as BBDCAfter
from forest import after_forest_save as ForestAfter
from github import after_github_save as GitHubAfter
from douban import after_douban_save as DoubanAfter
from reading import after_reading_save as ReadingAfter
from course import after_course_save as CourseAfter

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

# 豆瓣每日导入
@engine.define
def douban_daily_habit(**params):
	return DoubanCloud(params)

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

# GitHub hook
@engine.after_save('Douban')
def after_douban(_douban):
	return DoubanAfter(_douban)

# Reading hook
@engine.after_save('Reading')
def after_reading(_reading):
	return ReadingAfter(_reading)

# CourseAfter hook
@engine.after_save('Course')
def after_course(_course):
	return CourseAfter(_course)