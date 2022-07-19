#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : builder.py
@Author: Scott
@Date  : 2022/2/5 15:13
@Desc  : 自动化流程（flow）建造者
"""
import importlib
import json
from abc import ABCMeta, abstractmethod


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


class Builder(metaclass=ABCMeta):
    @abstractmethod
    def build(self):
        pass


class FlowBuilder(Builder):
    def __init__(self, flow_json_path):
        self.flow_json_path = flow_json_path
        self.constructed_object = {}
        self.name = ""

    def _get_handler_class(self, phase):
        """
        动态获取JSON流程文件中写的每个阶段处理的类
        :param phase:
        :return:
        """
        handler = phase["handler"].split(".")
        if len(handler) != 2:
            raise Exception("handler format is not right")
        module_name = handler[0]
        class_name = handler[1]
        handler_class = class_for_name(module_name, class_name)

        return handler_class

    def build(self):
        with open(self.flow_json_path, 'r', encoding='utf-8') as f:
            flow_json = json.load(f)
        self.name = flow_json["flow_name"]
        for phase in flow_json["phases"]:
            # 需要保存状态，所以不能是子进程的形式，只能由用户自己编写类后，这里动态加载类来执行
            handler_class = self._get_handler_class(phase)
            phase_name = phase["phase_name"]
            # TODO: python3.6版本之前字典不能保证顺序，要用ordered_dict
            self.constructed_object[phase_name] = (handler_class, phase["progress"])

        return 0
