# coding: utf-8

from leancloud import Engine
# from leancloud import LeanEngineError
# from forest import cloud as ForestCloud
from bbdc import bbdc_daily_habit as BBDCCloud
from forest import forest_daily_habit as ForestCloud
from bbdc import after_BBDC_save as BBDCAfter
from forest import after_forest_save as ForestAfter

engine = Engine()

# 不背单词每日导入
@engine.define
def bbdc_daily_habit(**params):
	return BBDCCloud(params)

# Forest每日导入
@engine.define
def forest_daily_habit(**params):
	return ForestCloud(params)

@engine.after_save('BBDC')
def after_BBDC(_bbdc):
	return BBDCAfter(_bbdc)

@engine.after_save('Forest')
def after_forest(_forest):
	return ForestAfter(_forest)