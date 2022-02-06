#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : scp_proxy.py
@Author: Scott
@Date  : 2022/2/6 18:08
@Desc  : 通过SCP上传/下载文件
"""
from scp import SCPClient
from relax.ssh_helper.client_proxy import SSHClientProxy


class SCPProxy:
    def __init__(self, log):
        self.log = log
        self.ssh_client = SSHClientProxy(log)

    def upload_file(self, remote_host, source_file_path, target_file_path):
        """
        向远端主机上传文件
        :param remote_host: SSHHost对象，表示远端主机地址
        :param source_file_path: 本地文件路径，必须是文件，不能是目录
        :param target_file_path: 要上传到的远端路径，可以是文件，也可以是目录（会上传到目录下）
        :return:
        """
        if self.ssh_client.set_remote_host(remote_host) != 0:
            self.log.error('user %s connect to remote host %s:%s failed' % (remote_host.username, remote_host.ip_addr,
                                                                            remote_host.port))
            return 1
        scp_client = SCPClient(self.ssh_client.get_transport())
        try:
            scp_client.put(source_file_path, target_file_path)
        except Exception as e:
            self.log.error("upload file [%s] to SSH server [%s] failed, error: %s" % (source_file_path,
                                                                                      target_file_path, str(e)))
            return 1
        # TODO: 异常时是否需要close
        scp_client.close()
        # try:
        #     transport = paramiko.Transport(ssh_client.get_transport())
        #     transport.connect(username=self.username, password=self.password)
        #     sftp = paramiko.SFTPClient.from_transport(transport)
        #     sftp.put(script_name, script_name)
        # except Exception as e:
        #     print(e)

        return 0

    def download_file(self, remote_host, remote_file_path, local_file_path):
        """
        从远端主机下载文件
        :param remote_host: SSHHost对象，表示远端主机地址
        :param remote_file_path: 远端文件路径，必须是文件，不能是目录
        :param local_file_path: 要下载到的本地路径，可以是文件，也可以是目录（会下载到目录下）
        :return:
        """
        if self.ssh_client.set_remote_host(remote_host) != 0:
            self.log.error('user %s connect to remote host %s:%s failed' % (remote_host.username, remote_host.ip_addr,
                                                                            remote_host.port))
            return 1
        scp_client = SCPClient(self.ssh_client.get_transport())
        try:
            scp_client.get(remote_file_path, local_file_path)
        except Exception as e:
            self.log.error("download file [%s] to local [%s] failed, error: %s" % (remote_file_path,
                                                                                   local_file_path, str(e)))
            return 1
        # TODO: 异常时是否需要close
        scp_client.close()

        return 0
