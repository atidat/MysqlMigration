#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import paramiko


# TODO support print exec_command operation result
class SSHExecutor:
    def __init__(self, host, user, passwd):
        self.ssh_cli = paramiko.SSHClient()
        self.ssh_cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_cli.connect(hostname=host, port=22, username=user, password=passwd)

    def mkdir_backup_dir(self, _dir):
        _, _, _, = self.ssh_cli.exec_command("mkdir -p %s" % _dir)

    def chown_mysql(self, src_dir):
        _, _, _, = self.ssh_cli.exec_command("chown -R mysql:mysql %s" % src_dir)

    # TODO must ensure that communicate without password between operate and slave is known by script user
    def scp_backup_dir(self, src_dir, sla_user, sla_ip, sla_dir):
        _, _, _, = self.ssh_cli.exec_command("cd %s && scp * %s@%s:%s" % (src_dir, sla_user, sla_ip, sla_dir))
        #print("cd %s && scp * %s@%s:%s" % (src_dir, sla_user, sla_ip, sla_dir))
        #print(out.read().decode())
        #print(err.read().decode())

    def gc(self):
        self.ssh_cli.close()
