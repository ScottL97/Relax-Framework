#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : director.py
@Author: Scott
@Date  : 2022/2/5 15:13
@Desc  : 自动化流程（flow）的director，负责组装和切换builder，以及运行和监控自动化流程
"""
import gc
from abc import ABCMeta, abstractmethod
from relax.flow.thread import FlowThread, FlowWatcherThread
from relax.tools.profiling import profiling


class Director(metaclass=ABCMeta):
    def __init__(self):
        self._builder = None

    def set_builder(self, builder):
        self._builder = builder

    def get_constructed_object(self):
        return self._builder.constructed_object

    @abstractmethod
    def construct(self):
        pass

    @abstractmethod
    def run(self):
        pass


class FlowDirector(Director):
    def __init__(self, log):
        super().__init__()
        self.log = log
        self._flow_thread = None
        self._flow_watcher_thread = None

        # flow开始、更新、完成的观察者集合
        self._start_callbacks = set()
        self._update_callbacks = set()
        self._complete_callbacks = set()

    def construct(self):
        try:
            self._builder.build()
        except Exception as e:
            self.log.error("Please check %s file, error: %s" % (self._builder.flow_json_path, str(e)))
            return 1

        return 0

    def get_flow_name(self):
        return self._builder.name

    def register_start_callback(self, callback):
        self._start_callbacks.add(callback)

    def register_update_callback(self, callback):
        self._update_callbacks.add(callback)

    def register_complete_callback(self, callback):
        self._complete_callbacks.add(callback)

    # 启动自动化线程，并启动一个线程等待替换线程结束后更新结果
    def start(self, flow_name):
        self._flow_thread = FlowThread(self.run, flow_name)
        self._flow_watcher_thread = FlowWatcherThread(self.watch_flow, flow_name)
        self._flow_thread.start()
        self._flow_watcher_thread.start()

    # 等待自动化线程返回结果，自动化线程返回值是None时表示自动化代码异常
    def watch_flow(self, flow_name):
        for start_callback in self._start_callbacks:
            start_callback(flow_name)
        self._flow_thread.join()
        for complete_callback in self._complete_callbacks:
            complete_callback(self._flow_thread.get_result(), flow_name)

    @profiling
    def run(self):
        ret = 0
        flow_name = self.get_flow_name()
        phases = self.get_constructed_object()

        self.log.phase("START FLOW %s" % flow_name)
        for phase_name in phases:
            self.log.phase("START PHASE %s" % phase_name)
            phase_class = phases[phase_name][0]
            phase_progress = phases[phase_name][1]
            phase = phase_class(self.log, phase_name, phase_progress)
            ret = phase.run()
            # 成功刷新进度条继续，失败返回非0值结束自动化流程
            if ret == 0:
                self.log.phase("%s SUCCESS" % phase_name)
                for update_callback in self._update_callbacks:
                    update_callback(phase)
            else:
                self.log.phase("%s FAIL" % phase_name)
                break
        gc.collect()
        self.log.phase("END FLOW %s" % flow_name)
        return ret
