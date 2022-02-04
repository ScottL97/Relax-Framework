#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : window.py
@Author: Scott
@Date  : 2022/2/2 16:59
@Desc  : 
"""
from abc import ABCMeta, abstractmethod


class Window(metaclass=ABCMeta):
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
    def enable_flow_buttons(self):
        """
        使所有flow按钮可用
        """
        pass

    @abstractmethod
    def disable_flow_buttons(self):
        """
        使所有flow按钮不可用
        """
        pass

    @abstractmethod
    def setup_phases(self, phases):
        """
        显示各阶段check button
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
    def append_log_to_textarea(self, level, line):
        """
        在textarea文本框中追加日志
        """
        pass

    @abstractmethod
    def setup_result(self, result):
        """
        显示自动化流程（flow）运行结果
        """
        pass
