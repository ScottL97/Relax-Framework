#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : client_proxy.py
@Author: Scott
@Date  : 2022/2/6 17:56
@Desc  : SSH客户端代理者
"""
import paramiko


SSH_CONNECT_TIMEOUT = 10


class SSHClientProxy:
    def __init__(self, log):
        self.log = log
        self.is_connected = False
        self.remote_host = None
        self.ssh_client = paramiko.SSHClient()
        # 允许连接不在~/.ssh/known_hosts文件中的主机
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # TODO: 哪些是用户调用的API，要通过某种方式告诉用户
    def set_remote_host(self, remote_host):
        self.remote_host = remote_host
        self.is_connected = False
        return self._connect_server()

    def get_transport(self):
        return self.ssh_client.get_transport()

    def get_root_password(self):
        return self.remote_host.root_password

    def exec_command(self, cmd, timeout=None, get_pty=False):
        return self.ssh_client.exec_command(cmd, timeout=timeout, get_pty=get_pty)

    def close(self):
        self.ssh_client.close()

    def _connect_server(self):
        """
        连接SSH服务器
        :return: 0 - 成功
                1 - 失败
        """
        try:
            self.ssh_client.connect(self.remote_host.ip_addr, self.remote_host.port, self.remote_host.username,
                                    self.remote_host.password, timeout=SSH_CONNECT_TIMEOUT)
        except Exception as e:
            self.log.error('ssh client connected to server failed: ' + str(e))
            return 1

        self.is_connected = True
        return 0
