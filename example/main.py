#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : main.py
@Author: Scott
@Date  : 2022/2/3 13:03
@Desc  : 
"""
import os
import sys

from relax.app import Relax

# 获取脚本或exe文件的执行路径
if getattr(sys, 'frozen', False):
    ROOT_PATH = os.path.dirname(sys.executable)
else:
    ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    r = Relax(ROOT_PATH)
    # 框架初始化，启动GUI
    r.init()
