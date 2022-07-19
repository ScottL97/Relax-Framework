#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : upload_images.py
@Author: Scott
@Date  : 2022/2/4 12:26
@Desc  : 
"""
from relax.flow.phase import Phase
from relax.log_manager.log import Log
import time


class ImagesUploader(Phase):
    def run(self):
        Log().info("ImagesUploader start")
        time.sleep(1)
        Log().info("ImagesUploader end")

        return 0

    def clean(self):
        return 0
