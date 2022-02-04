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

LEVEL_INFO = 0
LEVEL_WARN = 1
LEVEL_ERROR = 2
LEVEL_PHASE = 3


class Log:
    def __init__(self, log_file, window=None):
        self.log_file = log_file
        self.pid = os.getpid()
        self.window = window
        self.level = LEVEL_INFO

    def init(self):
        if self.log_file == '':
            return 1

        log_dirname = os.path.dirname(self.log_file)

        if not os.path.isdir(log_dirname):
            try:
                os.makedirs(log_dirname, 0o640)
            except Exception as e:
                print('make log dir %s failed: %s' % (log_dirname, str(e)))
                return 1

        return 0

    def set_level(self, level):
        self.level = level

    def _write_log(self, level, msg):
        line = '[%d] %s [%s] %s\n' % (self.pid, time.asctime(), level, msg)
        if self.window:
            self.window.append_log_to_textarea(level, line)
        with open(self.log_file, 'a') as f:
            f.write(line)

    def info(self, msg):
        if self.level > LEVEL_INFO:
            return
        self._write_log('INFO', msg)

    def warn(self, msg):
        if self.level > LEVEL_WARN:
            return
        self._write_log('WARN', msg)

    def error(self, msg):
        if self.level > LEVEL_PHASE:
            return
        self._write_log('ERROR', msg)

    def phase(self, msg):
        self._write_log('PHASE', '========%s========' % msg)
