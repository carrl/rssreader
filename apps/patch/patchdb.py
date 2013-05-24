#! /usr/bin/env python
#-*- coding:utf-8 -*-
# patch 資料庫

import string
import sqlite3
import sys

sys.path.append("../common")
import common


def patch001() :
    """ rss_detail 增加欄位 star ; 2013-05-22 """
    if (not common.checkfield("star", "rss_detail")) :
        dbname = common.getdbname()
        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        sql = "alter table rss_detail add column star boolean default 0"
        cursor.execute(sql)

        cursor.close()
        dbconn.close()

        print "patch 001 OK"


if __name__ == "__main__" :
    patch001()
