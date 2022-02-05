#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : __init__.py.py
@Author: Scott
@Date  : 2022/2/2 15:49
@Desc  : Relax框架单例类
"""
import sys
import os
from relax.log.log import Log
from relax.singleton.singleton import singleton
from relax.gui.tkinter_window import TkinterWindow
from relax.flow.mgr import FlowMgr

local_version = '0.1.0'


# TODO: 检查工具是否有新版本
# def check_if_expired():
#     global local_version
#     software_name = 'docker_auto_tool'
#
#     try:
#         config = configparser.RawConfigParser()
#         config.read(CONFIG_FILE_NAME, encoding='utf-8')
#         url = config.get('SERVER', 'version_check_url') + '?name=' + software_name
#     except Exception as e:
#         print('get version check url failed: ' + str(e))
#         return 1
#
#     with open('VERSION', 'r') as f:
#         local_version = f.read().strip('\n').strip()
#
#     try:
#         res = requests.get(url).json()
#         if res['result'] != 'ok':
#             return 1
#         print(res['version'] + '<->' + local_version)
#         if res['version'] != local_version:
#             messagebox.showinfo('软件更新提示', '发现新版本：%s，当前版本：%s，点击确定进行更新' % (res['version'], local_version))
#             if getattr(sys, 'frozen', False):
#                 subprocess.Popen('auto_update.exe %s %s %s' % (software_name + '.exe',
#                                                                res['version'], res['download_url']))
#             else:
#                 subprocess.Popen('python auto_update.py %s %s %s' % (software_name + '.exe',
#                                                                      res['version'], res['download_url']))
#             return 2
#     except Exception as e:
#         print('download software failed: ' + str(e))
#         return 1
#
#     return 0


# 更新工具版本
def upgrade_tool():
    return 0


@singleton
class Relax:
    def __init__(self, root_path):
        self.window = TkinterWindow()
        self.log = Log(os.path.join(root_path, 'relax.log'), self.window)
        self.flow_mgr = FlowMgr(root_path, self.log, self.window)

    def init(self):
        # 初始化日志
        if self.log.init() != 0:
            return 1
        # 自动更新工具版本
        ret = upgrade_tool()
        if ret == 0:
            print('已经是最新版本')
        elif ret == 1:
            print('检查更新失败')
        else:
            print('更新中，完成后自动启动')
            sys.exit(0)

        # 创建flow builder对象字典
        # TODO: 如果要实现动态加载JSON流程文件，这个方法需要每次点击按钮时调用，或者增加按钮调用该方法
        self.flow_mgr.init_flow_builders()
        # 启动GUI
        self.window.run()
