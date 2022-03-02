#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File  : command_executor.py
@Author: Scott
@Date  : 2022/2/6 18:28
@Desc  : 通过SSH远程执行命令
"""
import os
import shutil
import tempfile

from relax.file_transfer.scp_proxy import SCPProxy
from relax.ssh_proxy.client_proxy import SSHClientProxy

# TODO: 如果用户不属于sudoers、root用户禁止SSH登录、也没有expect，怎么办
# 用户不属于sudoers时也无法正常执行root权限命令，所以生成脚本，scp拷贝到远程，通过expect脚本升root权限执行
COMMON_SCRIPT = '''#!/bin/bash
%s
'''

# 使用root权限执行脚本
UTILS_SCRIPT = '''#!/bin/bash
exec_script_by_root() {
/usr/bin/expect<<EOF
spawn su -c "$@"
expect "*Password: "
send "%s\\r"
# interact
expect eof
EOF
}'''

SU_SCRIPT = '''#!/bin/bash
. %s/utils.sh
exec_script_by_root "./$1"'''

class SSHCommandResult:
    def __init__(self, stdin, stdout, stderr):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr


class SSHCommandExecutor:
    def __init__(self, log):
        self.log = log
        self.ssh_client = SSHClientProxy(log)
        self.tmp_dir = tempfile.TemporaryDirectory(dir='.').name
        self.root_cmd_executors = (self._exec_root_cmd_by_login_root, self._exec_root_cmd_by_sudo,
                                   self._exec_root_cmd_by_expect)

    def __del__(self):
        self._close()

    def _upload_script(self, remote_host, script_string, script_name):
        source_filename = os.path.join(self.tmp_dir, script_name)
        target_filename = "%s/%s" % (os.path.basename(self.tmp_dir), script_name)
        with open(source_filename, 'w') as f:
            f.write(script_string)

        scp_proxy = SCPProxy(self.log)
        if scp_proxy.upload_file(remote_host, source_filename, target_filename) != 0:
            return 1

        # TODO: 权限写死为550会导致切换其他用户组的用户后不能执行该脚本，但用户多数时间又不关心权限，怎么处理
        stdin, stdout, stderr = self.ssh_client.exec_command("chmod 550 " + target_filename)
        err = stderr.read().decode('utf8').strip()
        if len(err) != 0:
            self.log.error('change mod of %s failed: %s' % (target_filename, err))
        self.ssh_client.exec_command("sed -i -e 's/\r//' " + target_filename)

    def _upload_login_root_script(self, remote_host):
        utils_script = UTILS_SCRIPT % self.ssh_client.get_root_password()
        su_script = SU_SCRIPT % os.path.basename(self.tmp_dir)
        self._upload_script(remote_host, utils_script, 'utils.sh')
        self._upload_script(remote_host, su_script, 'su.sh')

    def _create_tmp_dir(self):
        self.log.info('tmp_dir: %s [%s]' % (self.tmp_dir, os.path.basename(self.tmp_dir)))
        # 服务器上创建存放脚本的临时目录
        try:
            os.mkdir(self.tmp_dir)
        except Exception as e:
            self.log.error('make local tmp dir %s failed: %s' % (os.path.basename(self.tmp_dir), str(e)))
            return 1
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command("mkdir %s" % os.path.basename(self.tmp_dir))
        except Exception as e:
            self.log.error('make remote tmp dir %s failed: %s' % (os.path.basename(self.tmp_dir), str(e)))
            return 1
        err = stderr.read().decode('utf8')
        if len(err) != 0:
            self.log.error('make remote tmp dir %s failed: %s' % (os.path.basename(self.tmp_dir), err))
            return 1

        return 0

    def exec_cmd(self, remote_host, cmd, is_use_root=False):
        """
        在服务器上执行shell命令
        :param SSHHost remote_host: 要执行命令的服务器信息
        :param str cmd: 执行的shell命令
        :param bool is_use_root: 是否执行root权限命令
        :return: str: string类型的标准输出
            str: string类型的标准错误
            int: 返回值，1 - 失败，0 - 成功
        """
        if is_use_root:
            result, err = self._exec_root_cmd(remote_host, cmd)
        else:
            result, err = self._exec_non_root_cmd(remote_host, cmd)
        if err != 0:
            return "", "", 1
        out_string, err_string = result.stdout.read().decode('utf8'), result.stderr.read().decode('utf8')

        return out_string, err_string, 0

    def _exec_root_cmd_by_login_root(self, remote_host, cmd):
        """
        通过root用户登录执行shell命令
        :param SSHHost remote_host: 要执行命令的服务器信息
        :param str cmd: 执行的shell命令
        :return: SSHCommandResult: 命令执行结果
            int: 返回值，1 - 失败，0 - 成功
        """
        if self.ssh_client.connect_remote_host(remote_host, is_use_root=True) != 0:
            self.log.error('user root connect to remote host %s:%s failed' % (remote_host.ip_addr, remote_host.port))
            return None, 1
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return SSHCommandResult(stdin, stdout, stderr), 0

    def _exec_root_cmd_by_sudo(self, remote_host, cmd):
        """
        使用普通用户登录执行sudo shell命令
        :param SSHHost remote_host: 要执行命令的服务器信息
        :param str cmd: 执行的shell命令
        :return: SSHCommandResult: 命令执行结果
            int: 返回值，1 - 失败，0 - 成功
        """
        if self.ssh_client.connect_remote_host(remote_host) != 0:
            self.log.error('user %s connect to remote host %s:%s failed' % (remote_host.username, remote_host.ip_addr,
                                                                            remote_host.port))
            return None, 1
        cmd = "sudo " + cmd
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        except Exception as e:
            self.log.error("exec root cmd by sudo failed: %s" % str(e))
            return None, 1
        if stderr.read().startswith(b'sudo: '):
            return None, 1
        return SSHCommandResult(stdin, stdout, stderr), 0

    def _exec_root_cmd_by_expect(self, remote_host, cmd):
        """
        通过expect脚本+root密码，使用普通用户登录执行shell命令
        :param SSHHost remote_host: 要执行命令的服务器信息
        :param str cmd: 执行的shell命令
        :return: SSHCommandResult: 命令执行结果
            int: 返回值，1 - 失败，0 - 成功
        """
        if self.ssh_client.connect_remote_host(remote_host) != 0:
            self.log.error('user %s connect to remote host %s:%s failed' % (remote_host.username, remote_host.ip_addr,
                                                                            remote_host.port))
            return None, 1
        self._create_tmp_dir()
        self._upload_login_root_script(remote_host)
        self._upload_script(remote_host, COMMON_SCRIPT % cmd, 'tmp.sh')
        tmp_dir_name = os.path.basename(self.tmp_dir)
        root_cmd = "%s/su.sh %s/tmp.sh" % (tmp_dir_name, tmp_dir_name)

        stdin, stdout, stderr = self.ssh_client.exec_command(root_cmd, get_pty=True)
        if stdout.read().find(b'/usr/bin/expect') != -1:
            self.log.error("there is no expect on server")
            return None, 1

        return SSHCommandResult(stdin, stdout, stderr), 0

    def _exec_root_cmd(self, remote_host, cmd):
        """
        尝试策略执行root命令，直到成功或尝试完所有的策略
        :param SSHHost remote_host: 要执行命令的服务器信息
        :param str cmd: 执行的shell命令
        :return: SSHCommandResult: 命令执行结果
            int: 返回值，1 - 失败，0 - 成功
        """
        for executor in self.root_cmd_executors:
            result, err = executor(remote_host, cmd)
            if err == 0:
                return result, 0
        self.log.error("exec root cmd failed")
        return None, 1

    def _exec_non_root_cmd(self, remote_host, cmd):
        # TODO: 同一host，每次执行命令都要连接一次，效率较低
        # TODO: 当连接了一台新的host时，旧的host的信息就丢失了，也就不会释放旧的host上的临时目录
        if self.ssh_client.connect_remote_host(remote_host) != 0:
            self.log.error('user %s connect to remote host %s:%s failed' % (remote_host.username, remote_host.ip_addr,
                                                                            remote_host.port))
            return None, 1
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        return SSHCommandResult(stdin, stdout, stderr), 0

    def _close(self):
        # TODO: 关闭窗口的时候，无法打印日志，会出异常
        stdin, stdout, stderr = self.ssh_client.exec_command("rm -rf %s" % os.path.basename(self.tmp_dir))
        err = stderr.read().decode('utf8')
        if len(err) != 0:
            self.log.error('rm -rf %s tmp dir on SSH server failed: %s' % (self.tmp_dir, err))
        if os.path.isdir(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
        self.ssh_client.close()
