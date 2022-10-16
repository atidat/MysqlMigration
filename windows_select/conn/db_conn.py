#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pymysql


class DBExecutor:
    def __init__(self, ip, port, user, passwd, database=None):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.descriptor = pymysql.connect(host=self.ip, port=int(self.port), user=self.user,
                                          password=self.passwd, database=self.database, local_infile=True)

    def __reconnect__(self, database=None):
        self.descriptor.close()
        self.descriptor = pymysql.connect(host=self.ip, port=int(self.port), user=self.user,
                                          password=self.passwd, database=database, local_infile=True)

    def reconnect(self):
        self.__reconnect__()

    def execute(self, sqls, database=None):
        res = []
        try:
            if (not self.database and database) or (self.database and not database):
                # print("reconnect database")
                self.__reconnect__(database)

            with self.descriptor.cursor() as cur:
                for sql in sqls:
                    cur.execute(sql)
                    res.append(cur.fetchall())
        except Exception as exc:
            print("Execute SQL:[%s] Catch Error: %s" % (sql[:10], exc))
            res = []
        finally:
            return res

    # TODO program corrupt, how to close db descriptor
    def gc(self):
        if not self.descriptor:
            self.descriptor.close()
