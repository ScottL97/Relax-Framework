#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : mgr.py
@Author: Scott
@Date  : 2022/2/4 19:20
@Desc  : 管理自动化流程，一个director通过设置不同的builder来切换自动化流程
"""
import os
from relax.flow.director import FlowDirector
from relax.flow.builder import FlowBuilder


class FlowMgr:
    def __init__(self, root_path, log, window):
        self.root_path = root_path
        self.flow_director = FlowDirector(log, window)
        self.flow_builders = {}
        self.log = log
        self.window = window

    def _construct_flow_builder(self, flow_json_path):
        flow_builder = FlowBuilder(self.log)
        self.flow_director.set_builder(flow_builder)
        if self.flow_director.construct(flow_json_path) != 0:
            return
        self.flow_builders[flow_builder.name] = flow_builder

    def init_flow_builders(self):
        """
        创建flow builder对象字典，字典的键为flow JSON文件中的flow_name，值为flow JSON文件中的phases解析后的结果
        一个flow JSON文件对应一个flow builder，需要启动某个flow（点击该flow的按钮）时，通过FlowDirector的set_builder方法切换flow
        """
        self.flow_builders = {}
        for root, dirs, files in os.walk(self.root_path):
            json_files = [file for file in files if file.endswith(".json")]
            for json_file in json_files:
                self._construct_flow_builder(os.path.join(root, json_file))
        self.window.init(self)

    def start_flow(self, flow_name):
        self.window.init(self)
        self.window.disable_flow_buttons()
        self.flow_director.set_builder(self.flow_builders[flow_name])
        self.window.setup_phases(self.flow_director.get_constructed_object())
        self.flow_director.start(flow_name)
