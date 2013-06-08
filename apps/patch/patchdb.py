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

def patch002() :
    """ 增加 table tags """
    dbname = common.getdbname()

    if (not common.checktable("tags")) :
        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        sql = """
create table if not exists tags (
        id integer primary key autoincrement,
        tname varcar
);
              """
        cursor.execute(sql)

        cursor.close()
        dbconn.close()

        print "patch 002 OK"

def patch003() :
    """ 增加 table tag_detail """
    dbname = common.getdbname()

    if (not common.checktable("tag_detail")) :
        dbconn = sqlite3.connect(dbname)
        cursor = dbconn.cursor()

        sql = """
create table if not exists tag_detail (
        id integer primary key autoincrement,
        tid integer,
        rid integer
);
              """
        cursor.execute(sql)

        cursor.close()
        dbconn.close()

        print "patch 003 OK"

if __name__ == "__main__" :
    patch001()
    patch002()
    patch003()
