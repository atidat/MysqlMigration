#!/bin/env python
# -*- coding: UTF-8 -*-

class Database_Const():
    def __init__(self):
        self.databases = "SELECT SCHEMA_NAME AS `Database` FROM INFORMATION_SCHEMA.SCHEMATA"
        self.create_database = "CREATE DATABASE %s"
        self.use_database = "use %s"

    def get_databases(self):
        return self.databases

    def get_create_database(self, database):
        return self.create_database % database

    def get_use_database(self, database):
        return self.use_database % database


class Table_Const():
    def __init__(self):
        self.tables_by_database = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='%s'"
        self.create_table = "SHOW CREATE TABLE %s.%s"
        self.select_into_file = "SELECT * FROM %s INTO OUTFILE '%s' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
        self.load_from_file = "LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"

    def get_tables_by_database(self, database):
        return self.tables_by_database % database

    def get_create_table(self, database, table):
        return self.create_table % (database, table)

    def backup_to_file(self, table, backup_file):
        return self.select_into_file % (table, backup_file)

    # TODO CRITICAL BUG: (1017, "Can't find file 'b'/var/lib/mysql-files/backup/bbigdata.sbtest4.csv''")
    # pretty sure the csv file is existed
    def restore_from_file(self, restore_file, table):
        return self.load_from_file % (str(restore_file), table)


class System_Database_Const():
    def __init__(self):
        self.system_databases = {"mysql", "sys", "performance_schema", "information_schema"}

    def get_system_databases(self):
        return self.system_databases

