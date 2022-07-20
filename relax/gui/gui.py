#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : window.py
@Author: Scott
@Date  : 2022/2/2 16:59
@Desc  : 
"""
from abc import ABCMeta, abstractmethod


class GUI(metaclass=ABCMeta):
    @abstractmethod
    def init(self, flow_mgr):
        """
        启动GUI以及每次点击自动化流程（flow）按钮时，初始化GUI
        """
        pass

    @abstractmethod
    def run(self):
        """
        运行GUI
        """
        pass

    @abstractmethod
    def setup_phases(self, phases):
        """
        显示流程的各阶段
        """
        pass

    @abstractmethod
    def set_progress(self, progress):
        """
        设置进度条的进度
        """
        pass

    @abstractmethod
    def set_phase(self, phase_name):
        """
        设置自动化流程当前已完成阶段
        """
        pass

    @abstractmethod
    def set_result(self, result):
        """
        设置自动化流程运行结果
        """
        pass

    @abstractmethod
    def write_log(self, level, line):
        """
        在GUI上写日志
        """
        pass
