#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os.path

from cons import sqls
from pathlib import Path


def backup_data(m_backup_dir, d2t, mde):
    print("====> start backup data")
    for database in d2t.keys():
        backup_sqls = []
        for table in d2t[database]:
            csv_path = os.path.join(m_backup_dir, "%s.%s.csv" % (database, table))
            csv_path = Path(csv_path).as_posix()
            backup_sqls.append(sqls.Table_Const().backup_to_file(table, csv_path))

        mde.execute(backup_sqls, database)
    print("====> end  backup data")


def restore_data(s_backup_dir, d2t, sde):
    print("====> start restore data")
    for database in d2t.keys():
        restore_sqls = []
        for table in d2t[database]:
            csv_path = os.path.join(s_backup_dir, "%s.%s.csv" % (database, table))
            csv_path = Path(csv_path).as_posix()
            restore_sqls.append(sqls.Table_Const().restore_from_file(csv_path, table))
        print("restore sqls are", restore_sqls)
        sde.execute(restore_sqls, database)
    print("====> end restore data")


def create_databases_tables(sde, d2ts):
    print("====> start create databases and tables")
    for database in d2ts.keys():
        sde.execute([sqls.Database_Const().get_create_database(database)])

    for database in d2ts.keys():
        for create_tables in d2ts[database]:
            sde.execute([create_tables[0][1]], database)
    print("====> end create databases and tables")


def set_local_infile(sde):
    print("====> start set local infile")
    sde.execute(["SET GLOBAL local_infile=1"])
    sde.reconnect()
    sde.execute(["show global variables like 'local_infile'"])
    print("====> end set local infile")


def get_create_database_table_sqls(mde, d2ts):
    print("====> start get create database table sqls")
    create_database_table_sqls = {}
    for database in d2ts.keys():
        show_create_tables = []
        for table in d2ts[database]:
            show_create_tables.append(sqls.Table_Const().get_create_table(database, table))

        create_tables = mde.execute(show_create_tables, database)
        create_tables = {cre_tab for cre_tab in create_tables}

        create_database_table_sqls[database] = create_tables
    print("====> end get create database table sqls")
    return create_database_table_sqls


def gen_databases_and_tables(mde):
    print("====> start generate databases and tables")
    d2ts = {}
    try:
        databases = mde.execute([sqls.Database_Const().get_databases()])
        databases = {database[0] for database in databases[0]
                     if database[0] not in sqls.System_Database_Const().get_system_databases()}

        for database in databases:
            tables = mde.execute([sqls.Table_Const().get_tables_by_database(database)])
            tables = {table[0] for table in tables[0]}
            d2ts[database] = tables

    except Exception as err:
        print("generate databases and tables meet error: %s" % err)
        d2ts = None
    finally:
        print("====> end generate databases and tables")
        return d2ts
