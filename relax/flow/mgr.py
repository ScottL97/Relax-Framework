#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : mgr.py
@Author: Scott
@Date  : 2022/2/4 19:20
@Desc  : 管理自动化流程，一个director通过设置不同的builder来切换自动化流程
"""
import os
from relax.log_manager.log import Log
from relax.flow.director import FlowDirector
from relax.flow.builder import FlowBuilder


class FlowMgr:
    def __init__(self, root_path, window):
        self.root_path = root_path
        self.flow_director = FlowDirector()
        self.flow_builders = {}
        self.window = window

    def _construct_flow_builder(self, flow_builder):
        self.flow_director.set_builder(flow_builder)
        if self.flow_director.construct() != 0:
            Log().error("construct %s failed" % flow_builder.flow_json_path)
            return 1
        return 0

    def _add_flow_builder_to_builders(self, flow_json_path):
        flow_builder = FlowBuilder(flow_json_path)
        if self._construct_flow_builder(flow_builder) != 0:
            return
        self.flow_builders[flow_builder.name] = flow_builder

    def init(self):
        self._init_flow_builders()
        self._register_observers()

    def _init_flow_builders(self):
        """
        创建flow builder对象字典，字典的键为flow JSON文件中的flow_name，值为flow JSON文件中的phases解析后的结果
        一个flow JSON文件对应一个flow builder，需要启动某个flow（点击该flow的按钮）时，通过FlowDirector的set_builder方法切换flow
        TODO: 如果要实现动态加载JSON流程文件，这个方法需要每次点击按钮时调用，或者增加按钮调用该方法
        """
        self.flow_builders = {}
        for root, dirs, files in os.walk(self.root_path):
            json_files = [file for file in files if file.endswith(".json")]
            for json_file in json_files:
                self._add_flow_builder_to_builders(os.path.join(root, json_file))
        self.window.init(self)

    def _register_observers(self):
        self.flow_director.register_start_callback(
            lambda flow_name: self.window.set_result('运行结果：[%s] 运行中' % flow_name)
        )

        def _update_window(phase):
            self.window.set_phase(phase.phase_name)
            self.window.set_progress(phase.progress)
        self.flow_director.register_update_callback(_update_window)

        self.flow_director.register_complete_callback(
            lambda result, flow_name: self.window.setup_result(result, flow_name)
        )

    def start_flow(self, flow_name):
        self.window.set_progress(0)
        if self._construct_flow_builder(self.flow_builders[flow_name]) != 0:
            return
        self.window.disable_flow_buttons()
        self.window.setup_phases(self.flow_director.get_constructed_object())
        self.flow_director.start(flow_name)
