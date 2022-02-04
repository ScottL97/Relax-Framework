#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : frame_progress_bar.py
@Author: Scott
@Date  : 2022/2/2 17:02
@Desc  : 
"""
import tkinter as tk
from tkinter import ttk


class FrameProgress(tk.Frame):
    def __init__(self, parent, **cnf):
        tk.Frame.__init__(self, master=parent, **cnf)
        bg = parent.cget("background")

        s = ttk.Style()
        s.theme_use("clam")
        # 颜色随偏好修改 部分设置只在特定主题有效果,否则为默认绿色
        s.configure(
            "fp.Horizontal.TProgressbar",
            troughcolor=bg,
            background="#0078d7",
            lightcolor="#0078d7",
            darkcolor="#0078d7",
            relief=tk.GROOVE
        )

        self.pBar = ttk.Progressbar(self,
                                    length=100,
                                    orient="horizontal",
                                    mode="determinate",
                                    style="fp.Horizontal.TProgressbar")

        # sticky="wens" 上面length 值会被忽略
        self.pBar.grid(row=0, column=0, sticky="wens")

        # 父组件的大小不由子组件决定
        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
