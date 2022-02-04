#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : update_images.py
@Author: Scott
@Date  : 2022/2/4 12:26
@Desc  : 
"""
from relax.flow.phase import Phase
import time


class ImagesUpdater(Phase):
    def run(self):
        self.log.info("ImagesUpdater start")
        time.sleep(1)
        self.log.info("ImagesUpdater end")

        return 0

    def clean(self):
        return 0
