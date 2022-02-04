#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : singleton.py
@Author: Scott
@Date  : 2022/2/2 16:13
@Desc  : 
"""
import threading


def singleton(cls):
    _instance = {}
    _instance_lock = threading.Lock()

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            with _instance_lock:
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kwargs)

        return _instance[cls]

    return _singleton
