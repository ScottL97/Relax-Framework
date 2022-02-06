#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : host.py
@Author: Scott
@Date  : 2022/2/6 17:57
@Desc  : SSH主机
"""


class SSHHost:
    def __init__(self, ip_addr, username, password, port=22, root_password=""):
        self.ip_addr = ip_addr
        self.username = username
        self.password = password
        self.port = port
        self.root_password = root_password
