#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : get_images.py
@Author: Scott
@Date  : 2022/2/4 11:52
@Desc  :
# TODO: 制作工具，根据JSON文件自动生成脚本和类
"""
from relax.flow.phase import Phase
from relax.log_manager.log import Log
import time


class ImagesAcquirer(Phase):
    def run(self):
        Log().info("ImagesAcquirer start")
        time.sleep(1)
        Log().info("ImagesAcquirer end")

        return 0

    def clean(self):
        return 0
