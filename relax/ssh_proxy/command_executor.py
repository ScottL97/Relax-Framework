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
from relax.ssh_helper.client_proxy import SSHClientProxy

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


class SSHCommandExecutor:
    def __init__(self, log):
        self.log = log
        self.ssh_client = SSHClientProxy(log)
        self.tmp_dir = tempfile.TemporaryDirectory(dir='.').name

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
        self.ssh_client.exec_command("dos2unix " + target_filename)

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
        stdin, stdout, stderr = self.ssh_client.exec_command("mkdir %s" % os.path.basename(self.tmp_dir))
        err = stderr.read().decode('utf8')
        if len(err) != 0:
            self.log.error('make remote tmp dir %s failed: %s' % (os.path.basename(self.tmp_dir), err))
            return 1

        return 0

    # 返回值：stdout字符串，stderr字符串，结果（0为成功，非0为失败）
    def exec_cmd(self, remote_host, cmd, use_root=False):
        if self.ssh_client.set_remote_host(remote_host) != 0:
            self.log.error('user %s connect to remote host %s:%s failed' % (remote_host.username, remote_host.ip_addr,
                                                                            remote_host.port))
            return 1
        # 执行命令
        if use_root:
            self._create_tmp_dir()
            self._upload_login_root_script(remote_host)
            self._upload_script(remote_host, COMMON_SCRIPT % cmd, 'tmp.sh')
            tmp_dir_name = os.path.basename(self.tmp_dir)
            root_cmd = "%s/su.sh %s/tmp.sh" % (tmp_dir_name, tmp_dir_name)
            stdin, stdout, stderr = self.ssh_client.exec_command(root_cmd, get_pty=True)
        else:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
        out, err = stdout.read().decode('utf8'), stderr.read().decode('utf8')

        return out, err, 0

    def close(self):
        if not self.ssh_client.is_connected:
            return
        stdin, stdout, stderr = self.ssh_client.exec_command("rm -rf %s" % os.path.basename(self.tmp_dir))
        err = stderr.read().decode('utf8')
        if len(err) != 0:
            self.log.error('rm -rf %s tmp dir on SSH server failed: %s' % (self.tmp_dir, err))
        shutil.rmtree(self.tmp_dir)
        self.ssh_client.close()
