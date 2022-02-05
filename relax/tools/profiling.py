#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : profiling.py
@Author: Scott
@Date  : 2022/2/5 17:09
@Desc  : 对函数执行时间进行计时
"""
import time
from functools import wraps


def profiling(f):
    @wraps(f)
    def _profiling(self, *args, **kwargs):
        start_time = time.time()
        result = f(self, *args, **kwargs)
        end_time = time.time()

        seconds = end_time - start_time
        minutes = seconds / 60
        seconds = seconds % 60
        self.log.phase("运行时间: %d 分 %d 秒" % (minutes, seconds))

        return result

    return _profiling
