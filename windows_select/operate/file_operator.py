#!/bin/env python
# -*- coding: UTF-8 -*-


def mkdir_chown_csv_backup_dir(mas_os_executor, sla_os_executor, mas_backup_dir, sla_backup_dir):
    # TODO ensure backup dir is not exist
    mas_os_executor.mkdir_backup_dir(mas_backup_dir)
    mas_os_executor.chown_mysql(mas_backup_dir)
    sla_os_executor.mkdir_backup_dir(sla_backup_dir)
    sla_os_executor.chown_mysql(sla_backup_dir)


# TODO
def rollback_mkdir_csv_backup_dir():
    pass


def scp_dir_from_master_2_slave(mas_os_executor, sla_os_executor, envs):
    print("====> start scp backup dir from master 2 slave")
    mas_os_executor.scp_backup_dir(envs.get("master_db_backup_dir"), envs.get("slave_os_user"),
                                   envs.get("slave_os_ip"), envs.get("slave_db_backup_dir"))
    sla_os_executor.chown_mysql(envs.get("slave_db_backup_dir"))
    print("====> end   scp backup dir from master 2 slave")
