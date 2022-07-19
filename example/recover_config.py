#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : recover_config.py
@Author: Scott
@Date  : 2022/2/4 12:27
@Desc  : 
"""
from relax.flow.phase import Phase
from relax.log_manager.log import Log
import time


class ConfigRecovery(Phase):
    def run(self):
        Log().info("ConfigRecovery start")
        time.sleep(1)
        Log().info("ConfigRecovery end")

        return 0

    def clean(self):
        return 0
