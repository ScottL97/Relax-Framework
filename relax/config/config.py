#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : config.py
@Author: Scott
@Date  : 2022/7/20 22:58
@Desc  : Relax框架配置单例类
"""
import configparser
import os
from relax.singleton.singleton import singleton
from relax.constant.constant import LOG_LEVEL, CONFIG_FILE_NAME


@singleton
class Config:
    """
    Relax框架配置项
    """
    def __init__(self, root_path=""):
        self._root_path = root_path
        self._server_ip = ""
        self._server_port = 0
        self._gui_mode = None
        self._log_level = LOG_LEVEL["INFO"]

    def load(self):
        # 读取配置文件
        config = configparser.ConfigParser()
        try:
            config.read(os.path.join(self._root_path, CONFIG_FILE_NAME))
        except Exception as e:
            print("read config failed:", str(e))
            return 1

        try:
            self._server_ip = config.get("CONF", "server.ip")
            self._server_port = int(config.get("CONF", "server.port"))
            self._gui_mode = config.get("CONF", "gui.mode")
            self._log_level = LOG_LEVEL[config.get("CONF", "log.level")]
        except Exception as e:
            print("get config failed:", str(e))
            return 1

        return 0

    def get_server_ip(self):
        return self._server_ip

    def get_server_port(self):
        return self._server_port

    def get_gui_mode(self):
        return self._gui_mode

    def get_log_level(self):
        return self._log_level
