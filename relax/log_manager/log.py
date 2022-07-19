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


@singleton
class Log:
    """
    单例模式的日志
    """
    _LEVEL_NUMBER = {
        "DEBUG": 0,
        "INFO": 1,
        "WARN": 2,
        "ERROR": 3,
        "PHASE": 4
    }

    def __init__(self, log_path=None, level=_LEVEL_NUMBER["INFO"]):
        self._log_path = log_path
        self._pid = os.getpid()
        self._level = level

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
            print("wrong log_manager dir:", os.path.dirname(self._log_path))
            return 1

        self.info("finish init log_manager")

        return 0

    def set_level(self, level):
        self._level = level

    def _write_log(self, level, *msg):
        if self._level > self._LEVEL_NUMBER[level]:
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
