#!/bin/env python
# -*- coding: UTF-8 -*-
import sys

from cfg import cfg
from operate import file_operator, db_operator
from conn import db_conn, ssh_conn


def prepare(envs):
    mas_os_executor = ssh_conn.SSHExecutor(envs.get("master_os_ip"), envs.get("master_os_user"), envs.get("master_os_passwd"))
    sla_os_executor = ssh_conn.SSHExecutor(envs.get("slave_os_ip"), envs.get("slave_os_user"), envs.get("slave_os_passwd"))
    mas_db_executor = db_conn.DBExecutor(envs.get("master_db_ip"), envs.get("master_db_port"),
                                         envs.get("master_db_user"), envs.get("master_db_passwd"))
    sla_db_executor = db_conn.DBExecutor(envs.get("slave_db_ip"), envs.get("slave_db_port"),
                                         envs.get("slave_db_user"), envs.get("slave_db_passwd"))
    return mas_os_executor, sla_os_executor, mas_db_executor, sla_db_executor


def run(mas_os_executor, sla_os_executor, mas_db_executor, sla_db_executor, envs):
    file_operator.mkdir_chown_csv_backup_dir(mas_os_executor, sla_os_executor,
                                             envs.get("master_db_backup_dir"), envs.get("slave_db_backup_dir"))

    databases_2_tables = db_operator.gen_databases_and_tables(mas_db_executor)
    db_operator.backup_data(envs.get("master_db_backup_dir"), databases_2_tables, mas_db_executor)

    file_operator.scp_dir_from_master_2_slave(mas_os_executor, sla_os_executor, envs)

    if not databases_2_tables:
        print("databases_2_tables is empty")
        sys.exit(1)  # T0D0 后续可定义为基于位的数值
    # print("databases and corresponding tables are: ", databases_2_tables)

    create_database_table_sqls = db_operator.get_create_database_table_sqls(mas_db_executor, databases_2_tables)
    if not create_database_table_sqls:
        print("create_database_table_sqls is empty")
        sys.exit(2)  # T0D0 后续可定义为基于位的数值
    # print(create_database_table_sqls)

    # TODO bug: database exist throw an exception
    db_operator.create_databases_tables(sla_db_executor, create_database_table_sqls)
    db_operator.set_local_infile(sla_db_executor)
    db_operator.restore_data(envs.get("slave_db_backup_dir"), databases_2_tables, sla_db_executor)


def gc(mas_os_executor, sla_os_executor, mas_db_executor, sla_db_executor):
    mas_os_executor.gc()
    sla_os_executor.gc()
    mas_db_executor.gc()
    sla_db_executor.gc()


if __name__ == '__main__':
    print("************ Welcome To Import Full MySQL Data ************")
    envs = cfg.parse_cfg_file()
    mas_os_executor, sla_os_executor, mas_db_executor, sla_db_executor = prepare(envs)
    run(mas_os_executor, sla_os_executor, mas_db_executor, sla_db_executor, envs)
    gc(mas_os_executor, sla_os_executor, mas_db_executor, sla_db_executor)
    print("************ Bye ************")
