# coding: utf-8
import sys
from datetime import datetime

import leancloud
from flask import Flask, jsonify, request
from flask import render_template
from flask_sockets import Sockets
from leancloud import LeanCloudError
import common
from views.todos import todos_view
from bbdc.api import BBDC
from forest.api import Forest
from lc.api import LC
from reading.api import Reading
from course.api import Course
from github.api import GitHub
from douban.api import Douban
app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')

# 开启跨域,用于debug
# from flask_cors import CORS
# CORS(app, supports_credentials=True)

sockets = Sockets(app)

# routing
app.register_blueprint(todos_view, url_prefix='/todos')

# @app.route('/bbdc')
# def bbdc():
#     return render_template('index.html')

@app.route('/')
def index():
	return render_template('index.html')

# 获取不背单词接口
@app.route('/api/bbdc', methods=['POST'])
def get_BBDC_data():
	bbdc = BBDC()
	try:
		page = request.get_json()['page']
	except Exception:
		page = 0
	datas = bbdc.get_lc_data(page)
	return jsonify(datas)

# 获取Forest接口
@app.route('/api/forest', methods=['POST'])
def get_forest_data():
	forest = Forest()
	try:
		page = request.get_json()['page']
	except Exception:
		page = 0
	datas = forest.get_lc_data(page)
	return jsonify(datas)

@app.route('/api/github', methods=['POST'])
def get_github_data():
	github = GitHub()
	try:
		page = request.get_json()['page']
	except Exception:
		page = 0
	datas = github.get_lc_data(page)
	return jsonify(datas)

@app.route('/api/douban', methods=['POST'])
def get_douban_data():
	douban = Douban()
	try:
		page = request.get_json()['page']
	except Exception:
		page = 0
	datas = douban.get_lc_data(page)
	return jsonify(datas)

@app.route('/api/reading', methods=['POST'])
def get_reading_data():
	reading = Reading()
	try:
		page = request.get_json()['page']
	except Exception:
		page = 0
	datas = reading.get_lc_data(page)
	return jsonify(datas)

@app.route('/api/course', methods=['POST'])
def get_course_data():
	course = Course()
	try:
		page = request.get_json()['page']
	except Exception:
		page = 0
	datas = course.get_lc_data(page)
	return jsonify(datas)

# 触发一次不背单词更新
@app.route('/api/doBBDC', methods=['POST'])
def do_BBDC():
	bbdc = BBDC()
	datas, numbers = bbdc.habitica_daily_export()
	res = {
		"numbers" : numbers,
		"msg" : datas
	}
	return jsonify(res)

# 触发一次 Forest 更新
@app.route('/api/doForest', methods=['POST'])
def do_Forest():
	forest = Forest()
	datas, numbers = forest.habitica_daily_export()
	res = {
		"numbers" : numbers,
		"msg" : datas
	}
	return jsonify(res)

# 触发一次 Github 更新
@app.route('/api/doGitHub', methods=['POST'])
def do_GitHub():
	github = GitHub()
	datas, numbers = github.habitica_daily_export()
	res = {
		"numbers" : numbers,
		"msg" : datas
	}
	return jsonify(res)

# 触发一次 Douban 更新
@app.route('/api/doDouban', methods=['POST'])
def do_Douban():
	douban = Douban()
	datas, numbers = douban.habitica_daily_export()
	res = {
		"numbers" : numbers,
		"msg" : datas
	}
	return jsonify(res)

# 触发一次 Reading 记录
@app.route('/api/doReading', methods=['POST'])
def do_Reading():
	reading = Reading()
	try:
		bookName = request.get_json()['bookName']
		bookPage = request.get_json()['bookPage']
	except Exception:
		return jsonify({
			"msg" : "参数错误"
		})
	datas, numbers = reading.habitica_export({
		"bookName" : bookName,
		"bookPage" : bookPage,
	})
	res = {
		"numbers" : numbers,
		"msg" : datas
	}
	return jsonify(res)

# 触发一次 Reading 记录
@app.route('/api/doCourse', methods=['POST'])
def do_Course():
	course = Course()
	try:
		courseName = request.get_json()['courseName']
		courseChapter = request.get_json()['courseChapter']
		courseSection = request.get_json()['courseSection']
	except Exception:
		return jsonify({
			"msg" : "参数错误"
		})
	datas, numbers = course.habitica_export({
		"courseName" : courseName,
		"courseChapter" : courseChapter,
		"courseSection" : courseSection,
	})
	res = {
		"numbers" : numbers,
		"msg" : datas
	}
	return jsonify(res)

# 获取项目数据
@app.route('/api/projects', methods=['POST'])
def get_projects():
	lc = LC()
	datas = lc.get_lc_projects()
	return jsonify(datas)

# 匹配所有路径
@app.route('/<path>')
def all(path):
	return render_template('index.html')