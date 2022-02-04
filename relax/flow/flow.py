#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : flow.py
@Author: Scott
@Date  : 2022/2/2 17:05
@Desc  : 
"""
import json
import importlib
from relax.flow.thread import FlowThread, FlowWatcherThread


def class_for_name(module_name, class_name):
    """
    通过字符串获取对应名称的类
    :param module_name: 模块名，即python文件名
    :param class_name: 类名
    :return:
    :exception: ImportError: 模块导入错误
                AttributeError: 类不存在
    """
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c


class Flow:
    def __init__(self, flow_json_path, log, window):
        self.flow_json_path = flow_json_path
        self.log = log
        self.window = window
        self.name = ''
        self.phases = {}
        self._flow_thread = None
        self._flow_watcher_thread = None

    # TODO: 计算时间的装饰器
    def run(self):
        ret = 0
        self.log.phase("START FLOW %s" % self.name)
        for phase_name in self.phases:
            self.log.phase("START PHASE %s" % phase_name)
            phase = self.phases[phase_name]
            ret = phase.run()
            phase.clean()
            # 成功刷新进度条继续，失败返回非0值
            if ret == 0:
                self.log.phase("%s SUCCESS" % phase_name)
                self.window.set_phase(phase_name)
                self.window.set_progress(phase.progress)
            else:
                self.log.phase("%s FAIL" % phase_name)
                break
        self.log.phase("END FLOW %s" % self.name)
        return ret

    def build(self):
        with open(self.flow_json_path, 'r', encoding='utf-8') as f:
            flow_json = json.load(f)
            self.name = flow_json["flow_name"]
            for phase_name in flow_json["phases"]:
                # TODO: 需要保存状态，所以不能是子进程的形式，只能由用户自己编写类后，这里动态加载类来执行
                handler_object = self._get_handler_object(flow_json["phases"][phase_name])
                if not handler_object:
                    return 1
                # TODO: 字典不能保证顺序，要用ordered_dict
                self.phases[phase_name] = handler_object

    def _get_handler_object(self, phase):
        """
        动态创建JSON流程文件中写的每个阶段处理的对象
        :param phase:
        :return:
        """
        handler = phase["handler"].split(".")
        if len(handler) != 2:
            return None
        module_name = handler[0]
        class_name = handler[1]
        try:
            handler_class = class_for_name(module_name, class_name)
        except (ModuleNotFoundError, AttributeError) as e:
            self.log.error("Please check %s file, error: %s" % (self.flow_json_path, str(e)))
            return None
        handler_object = handler_class(self.log, phase["progress"])

        return handler_object

    # 启动自动化线程，并启动一个线程等待替换线程结束后更新结果
    def start(self):
        self._flow_thread = FlowThread(self.run)
        self._flow_watcher_thread = FlowWatcherThread(self.watch_flow)
        self._flow_thread.start()
        self._flow_watcher_thread.start()

    # 等待自动化线程返回结果
    def watch_flow(self):
        self.window.set_result('运行结果：运行中')
        self._flow_thread.join()
        self.window.setup_result(self._flow_thread.get_result())
