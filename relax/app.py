#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : app.py
@Author: Scott
@Date  : 2022/2/2 15:49
@Desc  : Relax框架单例类
"""
import sys
from relax.log_manager.log import Log
from relax.singleton.singleton import singleton
from relax.gui.tkinter_window import TkinterWindow
from relax.flow.mgr import FlowMgr
from relax.config.config import Config

local_version = '0.1.0'
# TODO: 补充单元测试
# TODO: 增加WebsocketProxy，支持通过websocket发送自动化进度，注册到FlowDirector的观察者里
# TODO: 支持调用K8S的API实现K8S操作自动化
# TODO: 解耦FlowMgr和GUI


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
        self._root_path = root_path
        self._gui = None

    def _init_gui(self):
        gui_mode = Config().get_gui_mode()
        if gui_mode is None:
            Log().error("no GUI mode")
            return 1

        if gui_mode == "tkinter":
            # 初始化GUI
            self._gui = TkinterWindow()
            # 通过流程管理者初始化自动化流程及GUI
            FlowMgr(self._root_path, self._gui).init()
        else:
            Log().error("wrong GUI mode")
            return 1

        Log().register_callback(self._gui.write_log)
        return 0

    def init(self):
        # 初始化配置
        Config(self._root_path).load()
        # 自动更新工具版本
        ret = upgrade_tool()
        # TODO: 不要在这里处理返回值，更新时直接在upgrade_tool函数中退出
        if ret == 0:
            print('已经是最新版本')
        elif ret == 1:
            print('检查更新失败')
        else:
            print('更新中，完成后自动启动')
            sys.exit(0)
        # 初始化日志
        if Log(self._root_path).init() != 0:
            return 1
        # 根据配置初始化GUI
        if self._init_gui() != 0:
            return 1
        # 启动GUI
        self._gui.run()
