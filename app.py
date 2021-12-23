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
@app.route('/api/BBDC', methods=['POST'])
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