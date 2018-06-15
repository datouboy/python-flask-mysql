####!/usr/bin/python
# -*- coding: UTF-8 -*-

# flask，轻量级web框架
from flask import Flask
# Jinja2 模版，使用方法 render_template() 来渲染模版
from flask import render_template
# 加载自己编写的mysql models
from models.mysql_models import MysqlModels

app = Flask(__name__)

mysql_models = MysqlModels()

@app.route('/')
def indexPage():
    return 'Hello World!'

@app.route('/momo/')
def momoPage():
    array_list = mysql_models.selectList('again_goods','*','`ID` < 1000', 0, 5,'`ID` ASC')
    print(array_list)
    return 'Hello Momo!'

@app.route('/momo_photo/<picNum>')
def momoPhoto(picNum):
    # show the user profile for that user
    return 'PicNum %s' % picNum

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/my_momo/')
@app.route('/my_momo/<name>')
def hello(name=None):
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)