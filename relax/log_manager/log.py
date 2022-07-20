#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : log.py
@Author: Scott
@Date  : 2022/2/2 16:11
@Desc  : 日志类
"""
import os
import time
from relax.singleton.singleton import singleton
from relax.config.config import Config
from relax.constant.constant import LOG_LEVEL, LOG_FILE_NAME


@singleton
class Log:
    """
    单例模式的日志
    """

    def __init__(self, root_path=""):
        self._log_path = os.path.join(root_path, LOG_FILE_NAME)
        self._pid = os.getpid()
        self._level = Config().get_log_level()

        # 观察者集合，写日志时调用该集合中的所有callback函数
        self._callbacks = set()

    def register_callback(self, callback):
        """
        注册观察者
        :param callback: 观察者函数，需要两个参数，参数一为string类型，日志级别；参数二为string类型，日志打印的字符串
        :return: None
        """
        self._callbacks.add(callback)

    def init(self):
        if not os.path.isdir(os.path.dirname(self._log_path)):
            print("wrong log dir:", os.path.dirname(self._log_path))
            return 1

        self.info("finish init log")

        return 0

    def set_level(self, level):
        self._level = level

    def _write_log(self, level, *msg):
        if self._level > LOG_LEVEL[level]:
            return
        log_string = " ".join(msg)
        line = "[%d] %s [%s] %s\n" % (self._pid, time.asctime(), level, log_string)

        try:
            with open(self._log_path, "a") as f:
                f.write(line)
        except Exception as e:
            print("write log file failed:", str(e))

        for callback in self._callbacks:
            callback(level, log_string + "\n")

    def debug(self, *msg):
        self._write_log("DEBUG", *msg)

    def info(self, *msg):
        self._write_log("INFO", *msg)

    def warn(self, *msg):
        self._write_log("WARN", *msg)

    def error(self, *msg):
        self._write_log("ERROR", *msg)

    def phase(self, *msg):
        self._write_log("PHASE", "========", *msg, "========")

    def get_latest_logs(self):
        try:
            with open(self._log_path, "r") as f:
                logs = f.read()
        except Exception as e:
            print("get latest logs failed:", str(e))
            return ""

        return logs
