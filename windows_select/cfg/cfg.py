#!/bin/env python
# -*- coding: UTF-8 -*-

"""
parse os and database log-in configuration

cfg file name: mig.cnf
cfg file location: keep parent dir is the same with entrypoint script: main.py
cfg file example:
/ ***************************************
# database log in configuration
[database]
master_ip=103.169.103.201
master_user=root
master_port=3306
master_passwd=root

slave_ip=103.169.103.203
slave_user=root
slave_port=3306
slave_passwd=root

# IMPORTANT: backup_dir is same as database configuration
backup_dir=/var/lib/mysql-files

# database log in configuration
[system]
master_ip=103.169.103.201
master_user=root
master_passwd=123456

slave_ip=103.169.103.203
slave_user=root
slave_passwd=123456
*************************************** /

"""
import sys
import os.path
from pathlib import Path


# 单例
class Envs(object):
    def __init__(self):
        self.dicts = dict()

    def update(self, key, val):
        self.dicts[key] = val

    def get(self, key):
        return self.dicts[key]


def parse_cfg_file():
    cfg_file = os.path.join("", "mig.cnf")
    cfg_file = Path(cfg_file).as_posix()

    envs = Envs()
    with open(cfg_file) as cf:
        for line in cf.readlines():
            if line.isspace() or line.startswith("#") or line.startswith('['):
                continue
            line = line.strip()
            key, val = line.split("=")[0], line.split("=")[1]
            envs.update(key, val)
    return envs
