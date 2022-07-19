#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : phase.py
@Author: Scott
@Date  : 2022/2/4 11:45
@Desc  : 自动化流程（flow）的组成单元，用户编写每个阶段需要继承Phase抽象类
"""
from abc import ABCMeta, abstractmethod


class Phase(metaclass=ABCMeta):
    def __init__(self, phase_name, progress):
        self.phase_name = phase_name
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
