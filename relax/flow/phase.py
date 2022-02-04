#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : phase.py
@Author: Scott
@Date  : 2022/2/4 11:45
@Desc  : 
"""
from abc import ABCMeta, abstractmethod


class Phase(metaclass=ABCMeta):
    def __init__(self, log, progress):
        self.log = log
        self.progress = progress

    @abstractmethod
    def run(self):
        """
        执行阶段
        :return: 0 - 成功 非0 - 失败
        """
        pass

    @abstractmethod
    def clean(self):
        """
        清理临时文件
        :return: 0 - 成功 非0 - 失败
        """
        pass
