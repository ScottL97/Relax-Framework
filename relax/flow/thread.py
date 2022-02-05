#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : thread.py
@Author: Scott
@Date  : 2022/2/4 19:26
@Desc  : 自动化流程（flow）线程以及自动化流程监控线程
"""
import threading


class FlowThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func
        self._result = None

    def run(self):
        self._result = self.func()

    def get_result(self):
        return self._result


class FlowWatcherThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()
