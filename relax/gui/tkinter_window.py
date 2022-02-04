#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : tkinter_window.py
@Author: Scott
@Date  : 2022/2/4 19:49
@Desc  : 
"""
from relax.gui.window import Window
import random
import tkinter as tk
from tkinter import scrolledtext
from relax.gui.frame_progress_bar import FrameProgress
from relax.gui.widget import FlowButton, PhaseCheckButton

LOG_COLOR_DICT = {'ERROR': 'red',
                  'INFO': 'green',
                  'DEBUG': 'blue',
                  'PHASE': 'purple'}


class TkinterWindow(Window):
    def __init__(self):
        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)
        self.window.title("Relax")
        # self.window.geometry("800x600")

        # 阶段状态以及每个阶段的check button，当某阶段完成时标记为完成
        self.phase_check_buttons = {}

        # 运行状态显示
        self.result = tk.StringVar()
        self.result.set('运行结果：未运行')

        # top_frame显示运行结果
        self.top_frame = tk.Frame(self.window, relief=tk.RIDGE, bd=5, borderwidth=4)
        self.top_frame.pack(fill=tk.X, ipady=2, expand=False)

        # 在top_frame中添加flow按钮
        self.label = tk.Label(self.top_frame, textvariable=self.result)
        self.label.pack(padx=2, pady=20, side=tk.LEFT, anchor=tk.N)
        self.flow_buttons = {}

        # textarea用来显示日志
        self.textarea = scrolledtext.ScrolledText(self.window, state=tk.DISABLED)
        self.textarea.pack(fill=tk.X)

        # 自定义进度条
        self.progress_bar = FrameProgress(self.window, height=30, relief=tk.FLAT)
        self.progress_bar.pBar['maximum'] = 100
        self.progress_bar.pBar['value'] = 0
        self.progress_bar.pack(fill=tk.X)

        # phases_frame显示各阶段运行状态
        self.phases_frame = tk.Frame(self.window, relief=tk.RIDGE, bd=5, borderwidth=4)
        self.phases_frame.pack(fill=tk.X)

        # 自动化是否执行成功的标识符
        self.if_success = tk.BooleanVar()

    # 每次启动自动化流程时初始化GUI
    def init(self, flow_mgr):
        self.set_progress(0)
        self._setup_flow(flow_mgr)

    # 清除所有的flow按钮
    def _destroy_flow_buttons(self):
        for flow_name in self.flow_buttons:
            flow_button = self.flow_buttons[flow_name]
            flow_button.destroy()
        self.flow_buttons = {}

    # 清除所有的phase check button
    def _destroy_phase_check_buttons(self):
        for phase_name in self.phase_check_buttons:
            phase_button = self.phase_check_buttons[phase_name]
            phase_button.destroy()
        self.phase_check_buttons = {}

    # 在GUI上添加flow按钮
    def _setup_flow(self, flow_mgr):
        self._destroy_flow_buttons()
        for flow_name, flow in flow_mgr.flows.items():
            self.flow_buttons[flow_name] = FlowButton(flow_name, self.top_frame, flow_mgr.start_flow)
            self.flow_buttons[flow_name].show()
            # TODO: 有多个flow时，阶段会重复添加，怎么处理
            # self._setup_phases(flow.phases)

    # 设置GUI上显示的阶段
    def setup_phases(self, phases):
        self._destroy_phase_check_buttons()
        for phase_name in phases:
            self.phase_check_buttons[phase_name] = PhaseCheckButton(phase_name, self.phases_frame)
            self.phase_check_buttons[phase_name].show()

    def run(self):
        self.window.mainloop()

    def setup_result(self, result):
        if result == 0:
            self.set_result('运行结果：成功')
        elif result is None:
            self.set_result('运行结果：代码异常')
        else:
            # TODO: 显示失败的阶段
            self.set_result('运行结果：失败')
        self.enable_flow_buttons()

    def enable_flow_buttons(self):
        for flow_button in self.flow_buttons.values():
            flow_button.enable()

    def disable_flow_buttons(self):
        for flow_button in self.flow_buttons.values():
            flow_button.disable()

    # 设置运行结果
    def set_result(self, result):
        self.result.set(result)

    # 设置进度条
    def set_progress(self, progress):
        self.progress_bar.pBar['value'] = progress

    # 设置当前阶段
    def set_phase(self, phase_name):
        self.phase_check_buttons[phase_name].active()

    # 在文本框中追加日志
    def append_log_to_textarea(self, level, line):
        self.textarea.config(state=tk.NORMAL)
        tag_name = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 5))
        self.textarea.insert(tk.END, line, tag_name)
        self.textarea.tag_config(tag_name, foreground=LOG_COLOR_DICT[level])
        self.textarea.see(tk.END)
        self.textarea.config(state=tk.DISABLED)