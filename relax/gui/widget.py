#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : widget.py
@Author: Scott
@Date  : 2022/2/4 19:35
@Desc  : 
"""
import tkinter as tk


class PhaseCheckButton:
    def __init__(self, phase_name, phases_frame):
        self.status = tk.BooleanVar()
        self.check_button = tk.Checkbutton(phases_frame, text=phase_name + " =>", variable=self.status,
                                           state=tk.DISABLED)

    def active(self):
        self.status.set(True)

    def show(self):
        self.check_button.pack(padx=2, pady=20, side=tk.LEFT, anchor=tk.N)

    def destroy(self):
        self.check_button.destroy()


class FlowButton:
    def __init__(self, flow_name, flows_frame, handler):
        self.flow_name = flow_name
        self.flow_button = tk.Button(flows_frame, text=flow_name, command=self.start)
        self.handler = handler

    def start(self):
        self.handler(self.flow_name)

    def show(self):
        self.flow_button.pack(padx=2, pady=20, side=tk.RIGHT, anchor=tk.N)

    def destroy(self):
        self.flow_button.destroy()

    # 设置flow按钮属性为不可点击
    def disable(self):
        self.flow_button.config(state=tk.DISABLED)

    # 设置flow按钮属性为可点击
    def enable(self):
        self.flow_button.config(state=tk.NORMAL)
