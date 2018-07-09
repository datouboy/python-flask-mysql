####!/usr/bin/python3
# -*- coding: UTF-8 -*-
# @Time    : 2018/6/19
# @File    : print_top_desk.py.py

from PIL import ImageGrab #图像处理（截屏等功能）

class PrintTopDesk():

    def __init__(self):
        print('~~~~~~~~~~~~~~~~~~~~ PrintTopDesk Start ~~~~~~~~~~~~~~~~~~~~')

    #屏幕截图
    def printdesk(self):
        img = ImageGrab.grab()
        img.save('./static/images/desktop.jpeg')
        print('~~~~~~~~~~~~~~~~~~~~ TopDesk Print ~~~~~~~~~~~~~~~~~~~~')

if __name__ == '__main__':
    print('单独运行此文件，以下代码将被执行')
    # 使用方法：
    mmm = PrintTopDesk()
    mmm.printdesk()