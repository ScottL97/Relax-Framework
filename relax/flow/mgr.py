#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : mgr.py
@Author: Scott
@Date  : 2022/2/4 19:20
@Desc  : 
"""
import os
from relax.flow.flow import Flow


class FlowMgr:
    def __init__(self, root_path, log, window=None):
        self.root_path = root_path
        self.flows = {}
        self.log = log
        self.window = window

    def build_flows(self):
        self.flows = {}
        print(self.root_path)
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.endswith('.json'):
                    flow = Flow(os.path.join(root, file), self.log, self.window)
                    flow.build()
                    self.flows[flow.name] = flow
        self.window.init(self)

    def start_flow(self, flow_name):
        self.window.init(self)
        self.window.disable_flow_buttons()
        self.window.setup_phases(self.flows[flow_name].phases)
        self.flows[flow_name].start()
